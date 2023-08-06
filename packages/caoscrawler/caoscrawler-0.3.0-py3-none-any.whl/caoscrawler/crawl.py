#!/usr/bin/env python3
# encoding: utf-8
#
# ** header v3.0
# This file is a part of the CaosDB Project.
#
# Copyright (C) 2021 Henrik tom Wörden
#               2021 Alexander Schlemmer
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.
#
# ** end header
#

"""
Crawl a file structure using a yaml cfood definition and synchronize
the acuired data with CaosDB.
"""

from __future__ import annotations

import argparse
import importlib
import logging
import os
import sys
import uuid
import warnings
import yaml

from argparse import RawTextHelpFormatter
from collections import defaultdict
from copy import deepcopy
from enum import Enum
from importlib_resources import files
from jsonschema import validate
from typing import Any, Optional, Type, Union

import caosdb as db

from caosadvancedtools.cache import UpdateCache, Cache
from caosadvancedtools.crawler import Crawler as OldCrawler
from caosdb.apiutils import (compare_entities, EntityMergeConflictError,
                             merge_entities)
from caosdb.common.datatype import is_reference

from .converters import Converter, DirectoryConverter, ConverterValidationError
from .identifiable import Identifiable
from .identifiable_adapters import (IdentifiableAdapter,
                                    LocalStorageIdentifiableAdapter,
                                    CaosDBIdentifiableAdapter)
from .identified_cache import IdentifiedCache
from .macros import defmacro_constructor, macro_constructor
from .stores import GeneralStore, RecordStore
from .structure_elements import StructureElement, Directory, NoneElement
from .version import check_cfood_version

logger = logging.getLogger(__name__)

SPECIAL_PROPERTIES_STRICT = ("description", "name", "id", "path")
SPECIAL_PROPERTIES_NOT_STRICT = ("file", "checksum", "size")

# Register the macro functions from the submodule:
yaml.SafeLoader.add_constructor("!defmacro", defmacro_constructor)
yaml.SafeLoader.add_constructor("!macro", macro_constructor)


def check_identical(record1: db.Entity, record2: db.Entity, ignore_id=False):
    """
    This function uses compare_entities to check whether to entities are identical
    in a quite complex fashion:
    - If one of the entities has additional parents or additional properties -> not identical
    - If the value of one of the properties differs -> not identical
    - If datatype, importance or unit are reported different for a property by compare_entities
      return "not_identical" only if these attributes are set explicitely by record1.
      Ignore the difference otherwise.
    - If description, name, id or path appear in list of differences -> not identical.
    - If file, checksum, size appear -> Only different, if explicitely set by record1.

    record1 serves as the reference, so datatype, importance and unit checks are carried
    out using the attributes from record1. In that respect, the function is not symmetrical
    in its arguments.
    """
    comp = compare_entities(record1, record2)

    if ignore_id:
        if "id" in comp[0]:
            del comp[0]["id"]
        if "id" in comp[1]:
            del comp[1]["id"]

    for j in range(2):
        for label in ("parents", ):
            if len(comp[j][label]) > 0:
                return False
    for special_property in SPECIAL_PROPERTIES_STRICT:
        if special_property in comp[0] or special_property in comp[1]:
            return False

    for special_property in SPECIAL_PROPERTIES_NOT_STRICT:
        if special_property in comp[0]:
            attr_val = comp[0][special_property]
            other_attr_val = (comp[1][special_property]
                              if special_property in comp[1] else None)
            if attr_val is not None and attr_val != other_attr_val:
                return False

    for key in comp[0]["properties"]:
        if len(comp[0]["properties"][key]) == 0:
            # This is a new property
            return False
        for attribute in ("datatype", "importance", "unit"):
            # only make an update for those attributes if there is a value difference and
            # the value in the crawled_data is not None
            if attribute in comp[0]["properties"][key]:
                attr_val = comp[0]["properties"][key][attribute]
                other_attr_val = (comp[1]["properties"][key][attribute]
                                  if attribute in comp[1]["properties"][key] else None)
                if attr_val is not None and attr_val != other_attr_val:
                    return False

        if "value" in comp[0]["properties"][key]:
            return False

    # Check for removed properties:
    for key in comp[1]["properties"]:
        if len(comp[1]["properties"][key]) == 0:
            # This is a removed property
            return False

    return True


def _resolve_datatype(prop: db.Property, remote_entity: db.Entity):
    """ sets the datatype on the given property (side effect) """

    if remote_entity.role == "Property":
        datatype = remote_entity.datatype
    elif remote_entity.role == "RecordType":
        datatype = remote_entity.name
    else:
        raise RuntimeError("Cannot set datatype.")

    # Treat lists separately
    if isinstance(prop.value, list) and not datatype.startswith("LIST"):
        datatype = db.LIST(datatype)

    prop.datatype = datatype
    return prop


class SecurityMode(Enum):
    RETRIEVE = 0
    INSERT = 1
    UPDATE = 2


class Crawler(object):
    """
    Crawler class that encapsulates crawling functions.
    Furthermore it keeps track of the storage for records (record store) and the
    storage for values (general store).
    """

    def __init__(self,
                 generalStore: Optional[GeneralStore] = None,
                 debug: bool = False,
                 identifiableAdapter: IdentifiableAdapter = None,
                 securityMode: SecurityMode = SecurityMode.UPDATE
                 ):
        """
        Create a new crawler and initialize an empty RecordStore and GeneralStore.

        Parameters
        ----------
        recordStore : GeneralStore
             An initial GeneralStore which might store e.g. environment variables.
        debug : bool
             Create a debugging information tree when set to True.
             The debugging information tree is a variable stored in
             self.debug_tree. It is a dictionary mapping directory entries
             to a tuple of general stores and record stores which are valid for
             the directory scope.
             Furthermore, it is stored in a second tree named self.debug_copied whether the
             objects in debug_tree had been copied from a higher level in the hierarchy
             of the structureelements.
        identifiableAdapter : IdentifiableAdapter
             TODO describe
        securityMode : int
             Whether only retrieves are allowed or also inserts or even updates.
             Please use SecurityMode Enum
        """

        # The following caches store records, where we checked whether they exist on the remote
        # server. Since, it is important to know whether they exist or not, we store them into two
        # different caches.
        self.remote_existing_cache = IdentifiedCache()
        self.remote_missing_cache = IdentifiedCache()
        self.recordStore = RecordStore()
        self.securityMode = securityMode

        self.generalStore = generalStore
        if generalStore is None:
            self.generalStore = GeneralStore()

        self.identifiableAdapter: IdentifiableAdapter = LocalStorageIdentifiableAdapter()
        if identifiableAdapter is not None:
            self.identifiableAdapter = identifiableAdapter
        # If a directory is crawled this may hold the path to that directory
        self.crawled_directory: Optional[str] = None
        self.debug = debug
        if self.debug:
            # order in the tuple:
            # 0: generalStore
            # 1: recordStore
            self.debug_tree: dict[str, tuple] = dict()
            self.debug_metadata: dict[str, dict] = dict()
            self.debug_metadata["copied"] = dict()
            self.debug_metadata["provenance"] = defaultdict(lambda: dict())
            self.debug_metadata["usage"] = defaultdict(lambda: set())

    def load_definition(self, crawler_definition_path: str):
        """
        Load a cfood from a crawler definition defined by
        crawler definition path and validate it using cfood-schema.yml.
        """

        # Load the cfood from a yaml file:
        with open(crawler_definition_path, "r") as f:
            crawler_definitions = list(yaml.safe_load_all(f))

        crawler_definition = self._load_definition_from_yaml_dict(
            crawler_definitions)

        return self._resolve_validator_paths(crawler_definition, crawler_definition_path)

    def _load_definition_from_yaml_dict(self, crawler_definitions: list[dict]):
        """Load crawler definitions from a list of (yaml) dicts `crawler_definitions` which
        contains either one or two documents.

        Doesn't resolve the validator paths in the cfood definition, so for
        internal and testing use only.

        """
        if len(crawler_definitions) == 1:
            # Simple case, just one document:
            crawler_definition = crawler_definitions[0]
            metadata = {}
        elif len(crawler_definitions) == 2:
            metadata = crawler_definitions[0]["metadata"] if "metadata" in crawler_definitions[0] else {
            }
            crawler_definition = crawler_definitions[1]
        else:
            raise RuntimeError(
                "Crawler definition must not contain more than two documents.")

        check_cfood_version(metadata)

        # TODO: at this point this function can already load the cfood schema extensions
        #       from the crawler definition and add them to the yaml schema that will be
        #       tested in the next lines of code:

        # Load the cfood schema:
        with open(str(files('caoscrawler').joinpath('cfood-schema.yml')), "r") as f:
            schema = yaml.safe_load(f)

        # Add custom converters to converter enum in schema:
        if "Converters" in crawler_definition:
            for key in crawler_definition["Converters"]:
                schema["cfood"]["$defs"]["converter"]["properties"]["type"]["enum"].append(
                    key)
        if len(crawler_definitions) == 2:
            if "Converters" in metadata:
                for key in metadata["Converters"]:
                    schema["cfood"]["$defs"]["converter"]["properties"]["type"]["enum"].append(
                        key)

        # Validate the cfood schema:
        validate(instance=crawler_definition, schema=schema["cfood"])

        return crawler_definition

    def _resolve_validator_paths(self, definition: dict, definition_path: str):
        """Resolve path to validation files with respect to the file in which
        the crawler was defined.

        """

        for key, value in definition.items():

            if key == "validate" and isinstance(value, str):
                # Validator is given by a path
                if not value.startswith('/'):
                    # Not an absolute path
                    definition[key] = os.path.join(
                        os.path.dirname(definition_path), value)
                    if not os.path.isfile(definition[key]):
                        # TODO(henrik) capture this in `crawler_main` similar to
                        # `ConverterValidationError`.
                        raise FileNotFoundError(
                            f"Couldn't find validation file {definition[key]}")
            elif isinstance(value, dict):
                # Recursively resolve all validators
                definition[key] = self._resolve_validator_paths(
                    value, definition_path)

        return definition

    def load_converters(self, definition: dict):
        """
        Currently the converter registry is a dictionary containing for each converter:
        - key is the short code, abbreviation for the converter class name
        - module is the name of the module to be imported which must be installed
        - class is the converter class to load and associate with this converter entry

        all other info for the converter needs to be included in the converter plugin
        directory:
        schema.yml file
        README.md documentation
        """

        # Defaults for the converter registry:
        converter_registry: dict[str, dict[str, str]] = {
            "Directory": {
                "converter": "DirectoryConverter",
                "package": "caoscrawler.converters"},
            "SimpleFile": {
                "converter": "SimpleFileConverter",
                "package": "caoscrawler.converters"},
            "MarkdownFile": {
                "converter": "MarkdownFileConverter",
                "package": "caoscrawler.converters"},
            "File": {
                "converter": "SimpleFileConverter",
                "package": "caoscrawler.converters"},
            "JSONFile": {
                "converter": "JSONFileConverter",
                "package": "caoscrawler.converters"},
            "YAMLFile": {
                "converter": "YAMLFileConverter",
                "package": "caoscrawler.converters"},
            "CSVTableConverter": {
                "converter": "CSVTableConverter",
                "package": "caoscrawler.converters"},
            "XLSXTableConverter": {
                "converter": "XLSXTableConverter",
                "package": "caoscrawler.converters"},
            "DictBooleanElement": {
                "converter": "BooleanElementConverter",
                "package": "caoscrawler.converters"},
            "BooleanElement": {
                "converter": "BooleanElementConverter",
                "package": "caoscrawler.converters"},
            "DictFloatElement": {
                "converter": "FloatElementConverter",
                "package": "caoscrawler.converters"},
            "FloatElement": {
                "converter": "FloatElementConverter",
                "package": "caoscrawler.converters"},
            "DictTextElement": {
                "converter": "TextElementConverter",
                "package": "caoscrawler.converters"},
            "TextElement": {
                "converter": "TextElementConverter",
                "package": "caoscrawler.converters"},
            "DictIntegerElement": {
                "converter": "IntegerElementConverter",
                "package": "caoscrawler.converters"},
            "IntegerElement": {
                "converter": "IntegerElementConverter",
                "package": "caoscrawler.converters"},
            "DictListElement": {
                "converter": "ListElementConverter",
                "package": "caoscrawler.converters"},
            "ListElement": {
                "converter": "ListElementConverter",
                "package": "caoscrawler.converters"},
            "DictDictElement": {
                "converter": "DictElementConverter",
                "package": "caoscrawler.converters"},
            "DictElement": {
                "converter": "DictElementConverter",
                "package": "caoscrawler.converters"},
            "Dict": {
                "converter": "DictElementConverter",
                "package": "caoscrawler.converters"},
        }

        # More converters from definition file:
        if "Converters" in definition:
            for key, entry in definition["Converters"].items():
                if key in ["Dict", "DictTextElement", "DictIntegerElement", "DictBooleanElement",
                           "DictDictElement", "DictListElement", "DictFloatElement"]:
                    warnings.warn(DeprecationWarning(f"{key} is deprecated. Please use the new"
                                                     " variant; without 'Dict' prefix or "
                                                     "'DictElement' in case of 'Dict'"))

                converter_registry[key] = {
                    "converter": entry["converter"],
                    "package": entry["package"]
                }

        # Load modules and associate classes:
        for key, value in converter_registry.items():
            module = importlib.import_module(value["package"])
            value["class"] = getattr(module, value["converter"])
        return converter_registry

    def crawl_directory(self, dirname: str, crawler_definition_path: str):
        """ Crawl a single directory.

        Convenience function that starts the crawler (calls start_crawling)
        with a single directory as the StructureElement.
        """

        crawler_definition = self.load_definition(crawler_definition_path)
        # Load and register converter packages:
        converter_registry = self.load_converters(crawler_definition)

        if not dirname:
            raise ValueError(
                "You have to provide a non-empty path for crawling.")
        dir_structure_name = os.path.basename(dirname)
        self.crawled_directory = dirname
        if not dir_structure_name and dirname.endswith('/'):
            if dirname == '/':
                # Crawling the entire file system
                dir_structure_name = "root"
            else:
                # dirname had a trailing '/'
                dir_structure_name = os.path.basename(dirname[:-1])

        self.start_crawling(Directory(dir_structure_name,
                                      dirname),
                            crawler_definition,
                            converter_registry)

    @staticmethod
    def initialize_converters(crawler_definition: dict, converter_registry: dict):
        """
        takes the cfood as dict (`crawler_definition`) and creates the converter objects that
        are defined on the highest level. Child Converters will in turn be created during the
        initialization of the Converters.
        """
        converters = []

        for key, value in crawler_definition.items():
            # Definitions and Converters are reserved keywords
            # on the top level of the yaml file.
            # TODO: there should also be a top level keyword for the actual
            #       CFood to avoid confusion between top level keywords
            #       and the CFood.
            if key == "Definitions":
                continue
            elif key == "Converters":
                continue
            converters.append(Converter.converter_factory(
                value, key, converter_registry))

        return converters

    def start_crawling(self, items: Union[list[StructureElement], StructureElement],
                       crawler_definition: dict,
                       converter_registry: dict):
        """
        Start point of the crawler recursion.

        Parameters
        ----------
        items: list
             A list of structure elements (or a single StructureElement) that is used for
             generating the initial items for the crawler. This could e.g. be a Directory.
        crawler_definition : dict
             A dictionary representing the crawler definition, possibly from a yaml
             file.

        Returns
        -------
        crawled_data : list
            the final list with the target state of Records.
        """

        # This function builds the tree of converters out of the crawler definition.

        if self.generalStore is None:
            raise RuntimeError("Should not happen.")

        if not isinstance(items, list):
            items = [items]

        self.run_id = uuid.uuid1()
        local_converters = Crawler.initialize_converters(crawler_definition, converter_registry)

        # This recursive crawling procedure generates the update list:
        self.crawled_data: list[db.Record] = []
        self._crawl(items, local_converters, self.generalStore, self.recordStore, [], [])

        if self.debug:
            self.debug_converters = local_converters

        return self.crawled_data

    def synchronize(self, commit_changes: bool = True, unique_names=True):
        """
        Carry out the actual synchronization.
        """

        # After the crawling, the actual synchronization with the database, based on the
        # update list is carried out:

        return self._synchronize(self.crawled_data, commit_changes, unique_names=unique_names)

    def _has_reference_value_without_id(self, ident: Identifiable) -> bool:
        """
        Returns True if there is at least one value in the properties attribute of ``ident`` which:

        a) is a reference property AND
        b) where the value is set to a
           :external+caosdb-pylib:py:class:`db.Entity <caosdb.common.models.Entity>`
           (instead of an ID) AND
        c) where the ID of the value (the
           :external+caosdb-pylib:py:class:`db.Entity <caosdb.common.models.Entity>` object in b))
           is not set (to an integer)

        Returns
        -------
        bool
            True if there is a value without id (see above)

        Raises
        ------
        ValueError
            If no Identifiable is given.
        """
        if ident is None:
            raise ValueError("Identifiable has to be given as argument")
        for pvalue in list(ident.properties.values()) + ident.backrefs:
            if isinstance(pvalue, list):
                for el in pvalue:
                    if isinstance(el, db.Entity) and el.id is None:
                        return True
            elif isinstance(pvalue, db.Entity) and pvalue.id is None:
                return True
        return False

    @staticmethod
    def create_flat_list(ent_list: list[db.Entity], flat: Optional[list[db.Entity]] = None):
        """
        Recursively adds entities and all their properties contained in ent_list to
        the output list flat.

        TODO: This function will be moved to pylib as it is also needed by the
              high level API.
        """
        # Note: A set would be useful here, but we do not want a random order.
        if flat is None:
            flat = list()
        for el in ent_list:
            if el not in flat:
                flat.append(el)
        for ent in ent_list:
            for p in ent.properties:
                # For lists append each element that is of type Entity to flat:
                if isinstance(p.value, list):
                    for el in p.value:
                        if isinstance(el, db.Entity):
                            if el not in flat:
                                flat.append(el)
                                Crawler.create_flat_list([el], flat)
                elif isinstance(p.value, db.Entity):
                    if p.value not in flat:
                        flat.append(p.value)
                        Crawler.create_flat_list([p.value], flat)
        return flat

    def _has_missing_object_in_references(self, ident: Identifiable, referencing_entities: list):
        """
        returns False if any value in the properties attribute is a db.Entity object that
        is contained in the `remote_missing_cache`. If ident has such an object in
        properties, it means that it references another Entity, where we checked
        whether it exists remotely and it was not found.
        """
        if ident is None:
            raise ValueError("Identifiable has to be given as argument")
        for pvalue in list(ident.properties.values()) + ident.backrefs:
            # Entity instead of ID and not cached locally
            if (isinstance(pvalue, list)):
                for el in pvalue:
                    if (isinstance(el, db.Entity) and self.get_from_remote_missing_cache(
                            self.identifiableAdapter.get_identifiable(el, referencing_entities)) is not None):
                        return True
            if (isinstance(pvalue, db.Entity) and self.get_from_remote_missing_cache(
                    self.identifiableAdapter.get_identifiable(pvalue, referencing_entities)) is not None):
                # might be checked when reference is resolved
                return True
        return False

    def replace_references_with_cached(self, record: db.Record, referencing_entities: list):
        """
        Replace all references with the versions stored in the cache.

        If the cache version is not identical, raise an error.
        """
        for p in record.properties:
            if (isinstance(p.value, list)):
                lst = []
                for el in p.value:
                    if (isinstance(el, db.Entity) and el.id is None):
                        cached = self.get_from_any_cache(
                            self.identifiableAdapter.get_identifiable(el, referencing_entities))
                        if cached is None:
                            raise RuntimeError("Not in cache.")
                        if not check_identical(cached, el, True):
                            if isinstance(p.value, db.File):
                                if p.value.path != cached.path:
                                    raise RuntimeError("Not identical.")
                            else:
                                raise RuntimeError("Not identical.")
                        lst.append(cached)
                    else:
                        lst.append(el)
                p.value = lst
            if (isinstance(p.value, db.Entity) and p.value.id is None):
                cached = self.get_from_any_cache(
                    self.identifiableAdapter.get_identifiable(p.value, referencing_entities))
                if cached is None:
                    raise RuntimeError("Not in cache.")
                if not check_identical(cached, p.value, True):
                    if isinstance(p.value, db.File):
                        if p.value.path != cached.path:
                            raise RuntimeError("Not identical.")
                    else:
                        raise RuntimeError("Not identical.")
                p.value = cached

    def get_from_remote_missing_cache(self, identifiable: Identifiable):
        """
        returns the identified record if an identifiable with the same values already exists locally
        (Each identifiable that is not found on the remote server, is 'cached' locally to prevent
        that the same identifiable exists twice)
        """
        if identifiable is None:
            raise ValueError("Identifiable has to be given as argument")

        if identifiable in self.remote_missing_cache:
            return self.remote_missing_cache[identifiable]
        else:
            return None

    def get_from_any_cache(self, identifiable: Identifiable):
        """
        returns the identifiable if an identifiable with the same values already exists locally
        (Each identifiable that is not found on the remote server, is 'cached' locally to prevent
        that the same identifiable exists twice)
        """
        if identifiable is None:
            raise ValueError("Identifiable has to be given as argument")

        if identifiable in self.remote_existing_cache:
            return self.remote_existing_cache[identifiable]
        elif identifiable in self.remote_missing_cache:
            return self.remote_missing_cache[identifiable]
        else:
            return None

    def add_to_remote_missing_cache(self, record: db.Record, identifiable: Identifiable):
        """
        stores the given Record in the remote_missing_cache.

        If identifiable is None, the Record is NOT stored.
        """
        self.add_to_cache(record=record, cache=self.remote_missing_cache,
                          identifiable=identifiable)

    def add_to_remote_existing_cache(self, record: db.Record, identifiable: Identifiable):
        """
        stores the given Record in the remote_existing_cache.

        If identifiable is None, the Record is NOT stored.
        """
        self.add_to_cache(record=record, cache=self.remote_existing_cache,
                          identifiable=identifiable)

    def add_to_cache(self, record: db.Record, cache: IdentifiedCache,
                     identifiable: Identifiable) -> None:
        """
        stores the given Record in the given cache.

        If identifiable is None, the Record is NOT stored.
        """
        if identifiable is not None:
            cache.add(identifiable=identifiable, record=record)

    @staticmethod
    def bend_references_to_new_object(old, new, entities):
        """ Bend references to the other object
        Iterate over all entities in `entities` and check the values of all properties of
        occurances of old Entity and replace them with new Entity
        """
        for el in entities:
            for p in el.properties:
                if isinstance(p.value, list):
                    for index, val in enumerate(p.value):
                        if val is old:
                            p.value[index] = new
                else:
                    if p.value is old:
                        p.value = new

    @staticmethod
    def create_reference_mapping(flat: list[db.Entity]):
        """
        Create a dictionary of dictionaries of the form:
        dict[int, dict[str, list[db.Entity]]]

        - The integer index is the Python id of the value object.
        - The string is the name of the first parent of the referencing object.

        Each value objects is taken from the values of all properties from the list flat.

        So the returned mapping maps ids of entities to the objects which are referring
        to them.
        """
        # TODO we need to treat children of RecordTypes somehow.
        references: dict[int, dict[str, list[db.Entity]]] = {}
        for ent in flat:
            for p in ent.properties:
                val = p.value
                if not isinstance(val, list):
                    val = [val]
                for v in val:
                    if isinstance(v, db.Entity):
                        if id(v) not in references:
                            references[id(v)] = {}
                        if ent.parents[0].name not in references[id(v)]:
                            references[id(v)][ent.parents[0].name] = []
                        references[id(v)][ent.parents[0].name].append(ent)

        return references

    def split_into_inserts_and_updates(self, ent_list: list[db.Entity]):
        to_be_inserted: list[db.Entity] = []
        to_be_updated: list[db.Entity] = []
        flat = Crawler.create_flat_list(ent_list)

        # TODO: can the following be removed at some point
        for ent in flat:
            if ent.role == "Record" and len(ent.parents) == 0:
                raise RuntimeError("Records must have a parent.")

        resolved_references = True
        # flat contains Entities which could not yet be checked against the remote server
        while resolved_references and len(flat) > 0:
            resolved_references = False
            referencing_entities = self.create_reference_mapping(
                flat + to_be_updated + to_be_inserted)

            # For each element we try to find out whether we can find it in the server or whether
            # it does not yet exist. Since a Record may reference other unkown Records it might not
            # be possible to answer this right away.
            # The following checks are done on each Record:
            # 1. Can it be identified via an ID?
            # 2. Can it be identified via a path?
            # 3. Is it in the cache of already checked Records?
            # 4. Can it be checked on the remote server?
            # 5. Does it have to be new since a needed reference is missing?
            for i in reversed(range(len(flat))):
                record = flat[i]
                identifiable = self.identifiableAdapter.get_identifiable(
                    record,
                    referencing_entities=referencing_entities)

                # TODO remove if the exception is never raised
                if record in to_be_inserted:
                    raise RuntimeError("This should not be reached since treated elements"
                                       "are removed from the list")
                # 1. Can it be identified via an ID?
                elif record.id is not None:
                    to_be_updated.append(record)
                    self.add_to_remote_existing_cache(record, identifiable)
                    del flat[i]
                # 2. Can it be identified via a path?
                elif record.path is not None:
                    existing = self._get_entity_by_path(record.path)
                    if existing is None:
                        to_be_inserted.append(record)
                        self.add_to_remote_missing_cache(record, identifiable)
                        del flat[i]
                    else:
                        record.id = existing.id
                        # TODO check the following copying of _size and _checksum
                        # Copy over checksum and size too if it is a file
                        record._size = existing._size
                        record._checksum = existing._checksum
                        to_be_updated.append(record)
                        self.add_to_remote_existing_cache(record, identifiable)
                        del flat[i]
                # 3. Is it in the cache of already checked Records?
                elif self.get_from_any_cache(identifiable) is not None:
                    # We merge the two in order to prevent loss of information
                    newrecord = self.get_from_any_cache(identifiable)
                    try:
                        merge_entities(newrecord, record)
                    except EntityMergeConflictError:
                        continue
                    Crawler.bend_references_to_new_object(
                        old=record, new=newrecord, entities=flat + to_be_updated + to_be_inserted)

                    del flat[i]
                    resolved_references = True

                # 4. Can it be checked on the remote server?
                elif not self._has_reference_value_without_id(identifiable):
                    identified_record = (
                        self.identifiableAdapter.retrieve_identified_record_for_identifiable(
                            identifiable))
                    if identified_record is None:
                        # identifiable does not exist remotely -> record needs to be inserted
                        to_be_inserted.append(record)
                        self.add_to_remote_missing_cache(record, identifiable)
                        del flat[i]
                    else:
                        # side effect
                        record.id = identified_record.id
                        to_be_updated.append(record)
                        self.add_to_remote_existing_cache(record, identifiable)
                        del flat[i]
                    resolved_references = True

                # 5. Does it have to be new since a needed reference is missing?
                # (Is it impossible to check this record because an identifiable references a
                # missing record?)
                elif self._has_missing_object_in_references(identifiable, referencing_entities):
                    to_be_inserted.append(record)
                    self.add_to_remote_missing_cache(record, identifiable)
                    del flat[i]
                    resolved_references = True

            for record in flat:
                self.replace_references_with_cached(record, referencing_entities)

        if len(flat) > 0:
            raise RuntimeError(
                "Could not resolve all Entity references. Circular Dependency?")

        return to_be_inserted, to_be_updated

    def replace_entities_with_ids(self, rec: db.Record):
        for el in rec.properties:
            if isinstance(el.value, db.Entity):
                if el.value.id is not None:
                    el.value = el.value.id
            elif isinstance(el.value, list):
                for index, val in enumerate(el.value):
                    if isinstance(val, db.Entity):
                        if val.id is not None:
                            el.value[index] = val.id

    @staticmethod
    def _merge_properties_from_remote(
            crawled_data: list[db.Record],
            identified_records: list[db.Record]
    ):
        """Merge entity representation that was created by crawling the data with remotely found
        identified records s.th. new properties and property values are updated correctly but
        additional properties are not overwritten.

        Parameters
        ----------
        crawled_data : list[db.Record]
            List of the Entities  created by the crawler
        identified_records : list[db.Record]
            List of identified remote Records

        Returns
        -------
        to_be_updated : list[db.Record]
            List of merged records
        """
        to_be_updated = []
        for target, identified in zip(crawled_data, identified_records):
            # Special treatment for name and description in case they have been
            # set in the server independently from the crawler
            for attr in ["name", "description"]:
                if getattr(target, attr) is None:
                    # The crawler didn't find any name or description, i.e., not
                    # an empty one. In this case (and only in this), keep any
                    # existing name or description.
                    setattr(target, attr, getattr(identified, attr))

            # Create a temporary copy since the merge will be conducted in place
            tmp = deepcopy(identified)
            # A force merge will overwrite any properties that both the
            # identified and the crawled record have with the values of the
            # crawled record while keeping existing properties intact.
            merge_entities(tmp, target, force=True)
            to_be_updated.append(tmp)

        return to_be_updated

    @staticmethod
    def remove_unnecessary_updates(
            crawled_data: list[db.Record],
            identified_records: list[db.Record]
    ):
        """Compare the Records to be updated with their remote
        correspondant. Only update if there are actual differences.

        Returns
        -------
        update list without unecessary updates

        """
        if len(crawled_data) != len(identified_records):
            raise RuntimeError("The lists of updates and of identified records need to be of the "
                               "same length!")
        actual_updates = []
        for i in reversed(range(len(crawled_data))):

            if not check_identical(crawled_data[i], identified_records[i]):
                actual_updates.append(crawled_data[i])

        return actual_updates

    @staticmethod
    def execute_parent_updates_in_list(to_be_updated, securityMode, run_id, unique_names):
        """
        Execute the updates of changed parents.

        This method is used before the standard inserts and needed
        because some changes in parents (e.g. of Files) might fail
        if they are not updated first.
        """
        Crawler.set_ids_and_datatype_of_parents_and_properties(to_be_updated)
        parent_updates = db.Container()

        for record in to_be_updated:
            old_entity = Crawler._get_entity_by_id(record.id)

            # Check whether the parents have been changed and add them if missing
            # in the old entity:
            changes_made = False
            for parent in record.parents:
                found = False
                for old_parent in old_entity.parents:
                    if old_parent.id == parent.id:
                        found = True
                        break
                if not found:
                    old_entity.add_parent(id=parent.id)
                    changes_made = True
            if changes_made:
                parent_updates.append(old_entity)
        logger.debug("RecordTypes need to be added to the following entities:")
        logger.debug(parent_updates)
        if len(parent_updates) > 0:
            if securityMode.value > SecurityMode.INSERT.value:
                parent_updates.update(unique=False)
            elif run_id is not None:
                update_cache = UpdateCache()
                update_cache.insert(parent_updates, run_id)
                logger.info("Some entities need to be updated because they are missing a parent "
                            "RecordType. The update was NOT executed due to the chosen security "
                            "mode. This might lead to a failure of inserts that follow.")
                logger.info(parent_updates)

    @staticmethod
    def _get_entity_by_name(name):
        return db.Entity(name=name).retrieve()

    @staticmethod
    def _get_entity_by_path(path):
        try:
            return db.execute_query(f"FIND FILE WHICH IS STORED AT '{path}'", unique=True)
        except db.exceptions.EmptyUniqueQueryError:
            return None

    @staticmethod
    def _get_entity_by_id(id):
        return db.Entity(id=id).retrieve()

    @staticmethod
    def execute_inserts_in_list(to_be_inserted, securityMode, run_id: uuid.UUID = None,
                                unique_names=True):
        for record in to_be_inserted:
            for prop in record.properties:
                entity = Crawler._get_entity_by_name(prop.name)
                _resolve_datatype(prop, entity)
        logger.debug("INSERT")
        logger.debug(to_be_inserted)
        if len(to_be_inserted) > 0:
            if securityMode.value > SecurityMode.RETRIEVE.value:
                db.Container().extend(to_be_inserted).insert(unique=unique_names)
            elif run_id is not None:
                update_cache = UpdateCache()
                update_cache.insert(to_be_inserted, run_id, insert=True)

    @staticmethod
    def set_ids_and_datatype_of_parents_and_properties(rec_list):
        for record in rec_list:
            for parent in record.parents:
                if parent.id is None:
                    parent.id = Crawler._get_entity_by_name(parent.name).id
            for prop in record.properties:
                if prop.id is None:
                    entity = Crawler._get_entity_by_name(prop.name)
                    prop.id = entity.id
                    _resolve_datatype(prop, entity)

    @staticmethod
    def execute_updates_in_list(to_be_updated, securityMode, run_id: uuid.UUID = None,
                                unique_names=True):
        Crawler.set_ids_and_datatype_of_parents_and_properties(to_be_updated)
        logger.debug("UPDATE")
        logger.debug(to_be_updated)
        if len(to_be_updated) > 0:
            if securityMode.value > SecurityMode.INSERT.value:
                db.Container().extend(to_be_updated).update(unique=unique_names)
            elif run_id is not None:
                update_cache = UpdateCache()
                update_cache.insert(to_be_updated, run_id)

    def _synchronize(self, crawled_data: list[db.Record], commit_changes: bool = True,
                     unique_names=True):
        """
        This function applies several stages:
        1) Retrieve identifiables for all records in crawled_data.
        2) Compare crawled_data with existing records.
        3) Insert and update records based on the set of identified differences.

        This function makes use of an IdentifiableAdapter which is used to retrieve
        register and retrieve identifiables.

        if commit_changes is True, the changes are synchronized to the CaosDB server.
        For debugging in can be useful to set this to False.

        Return the final to_be_inserted and to_be_updated as tuple.
        """

        to_be_inserted, to_be_updated = self.split_into_inserts_and_updates(crawled_data)
        referencing_entities = self.create_reference_mapping(to_be_updated + to_be_inserted)

        # TODO: refactoring of typo
        for el in to_be_updated:
            # all entity objects are replaced by their IDs except for the not yet inserted ones
            self.replace_entities_with_ids(el)

        identified_records = [
            self.identifiableAdapter.retrieve_identified_record_for_record(record,
                                                                           referencing_entities)
            for record in to_be_updated]
        # Merge with existing data to prevent unwanted overwrites
        to_be_updated = self._merge_properties_from_remote(to_be_updated,
                                                           identified_records)
        # remove unnecessary updates from list by comparing the target records
        # to the existing ones
        to_be_updated = self.remove_unnecessary_updates(
            to_be_updated, identified_records)

        if commit_changes:
            self.execute_parent_updates_in_list(to_be_updated, securityMode=self.securityMode,
                                                run_id=self.run_id, unique_names=unique_names)
            self.execute_inserts_in_list(
                to_be_inserted, self.securityMode, self.run_id, unique_names=unique_names)
            self.execute_updates_in_list(
                to_be_updated, self.securityMode, self.run_id, unique_names=unique_names)

        update_cache = UpdateCache()
        pending_inserts = update_cache.get_inserts(self.run_id)
        if pending_inserts:
            Crawler.inform_about_pending_changes(
                pending_inserts, self.run_id, self.crawled_directory)

        pending_updates = update_cache.get_updates(self.run_id)
        if pending_updates:
            Crawler.inform_about_pending_changes(
                pending_updates, self.run_id, self.crawled_directory)

        return (to_be_inserted, to_be_updated)

    @staticmethod
    def inform_about_pending_changes(pending_changes, run_id, path, inserts=False):
        # Sending an Email with a link to a form to authorize updates is
        # only done in SSS mode

        if "SHARED_DIR" in os.environ:
            filename = OldCrawler.save_form(
                [el[3] for el in pending_changes], path, run_id)
            OldCrawler.send_mail([el[3] for el in pending_changes], filename)

        for i, el in enumerate(pending_changes):

            logger.debug(
                """
UNAUTHORIZED UPDATE ({} of {}):
____________________\n""".format(i + 1, len(pending_changes)) + str(el[3]))
        logger.info("There were unauthorized changes (see above). An "
                    "email was sent to the curator.\n"
                    "You can authorize the " +
                    ("inserts" if inserts else "updates")
                    + " by invoking the crawler"
                    " with the run id: {rid}\n".format(rid=run_id))

    @staticmethod
    def debug_build_usage_tree(converter: Converter):
        res: dict[str, dict[str, Any]] = {
            converter.name: {
                "usage": ", ".join(converter.metadata["usage"]),
                "subtree": {}
            }
        }

        for subconv in converter.converters:
            d = Crawler.debug_build_usage_tree(subconv)
            k = list(d.keys())
            if len(k) != 1:
                raise RuntimeError(
                    "Unkonwn error during building of usage tree.")
            res[converter.name]["subtree"][k[0]] = d[k[0]]
        return res

    def save_debug_data(self, filename: str):
        paths: dict[str, Union[dict, list]] = dict()

        def flatten_debug_info(key):
            mod_info = self.debug_metadata[key]
            paths[key] = dict()
            for record_name in mod_info:
                if key == "provenance":
                    paths[key][record_name] = dict()
                    for prop_name in mod_info[record_name]:
                        paths[key][record_name][prop_name] = {
                            "structure_elements_path": "/".join(
                                mod_info[record_name][prop_name][0]),
                            "converters_path": "/".join(
                                mod_info[record_name][prop_name][1])}
                elif key == "usage":
                    paths[key][record_name] = ", ".join(mod_info[record_name])
        for key in ("provenance", "usage"):
            flatten_debug_info(key)

        paths["converters_usage"] = [self.debug_build_usage_tree(
            cv) for cv in self.debug_converters]

        with open(filename, "w") as f:
            f.write(yaml.dump(paths, sort_keys=False))

    def _crawl(self, items: list[StructureElement],
               local_converters: list[Converter],
               generalStore: GeneralStore,
               recordStore: RecordStore,
               structure_elements_path: list[str], converters_path: list[str]):
        """
        Crawl a list of StructureElements and apply any matching converters.

        items: structure_elements (e.g. files and folders on one level on the hierarchy)
        local_converters: locally defined converters for
                            treating structure elements. A locally defined converter could be
                            one that is only valid for a specific subtree of the originally
                            cralwed StructureElement structure.
        generalStore and recordStore: This recursion of the crawl function should only operate on copies of the
                            global stores of the Crawler object.
        """
        for element in items:
            for converter in local_converters:

                # type is something like "matches files", replace isinstance with "type_matches"
                # match function tests regexp for example
                if (converter.typecheck(element) and
                        converter.match(element) is not None):
                    generalStore_copy = generalStore.create_scoped_copy()
                    recordStore_copy = recordStore.create_scoped_copy()

                    # Create an entry for this matched structure element:
                    generalStore_copy[converter.name] = (
                        os.path.join(*(structure_elements_path + [element.get_name()])))

                    # extracts values from structure element and stores them in the
                    # variable store
                    converter.create_values(generalStore_copy, element)

                    keys_modified = converter.create_records(
                        generalStore_copy, recordStore_copy, element)

                    children = converter.create_children(generalStore_copy, element)

                    if self.debug:
                        # add provenance information for each varaible
                        self.debug_tree[str(element)] = (
                            generalStore_copy.get_storage(), recordStore_copy.get_storage())
                        self.debug_metadata["copied"][str(element)] = (
                            generalStore_copy.get_dict_copied(),
                            recordStore_copy.get_dict_copied())
                        self.debug_metadata["usage"][str(element)].add(
                            "/".join(converters_path + [converter.name]))
                        mod_info = self.debug_metadata["provenance"]
                        for record_name, prop_name in keys_modified:
                            # TODO: check
                            internal_id = recordStore_copy.get_internal_id(
                                record_name)
                            record_identifier = record_name + \
                                "_" + str(internal_id)
                            converter.metadata["usage"].add(record_identifier)
                            mod_info[record_identifier][prop_name] = (
                                structure_elements_path + [element.get_name()],
                                converters_path + [converter.name])

                    self._crawl(children, converter.converters,
                                generalStore_copy, recordStore_copy,
                                structure_elements_path + [element.get_name()],
                                converters_path + [converter.name])
        # if the crawler is running out of scope, copy all records in
        # the recordStore, that were created in this scope
        # to the general update container.
        scoped_records = recordStore.get_records_current_scope()
        for record in scoped_records:
            self.crawled_data.append(record)

        # TODO: the scoped variables should be cleaned up as soon if the variables
        #       are no longer in the current scope. This can be implemented as follows,
        #       but this breaks the test "test_record_structure_generation", because
        #       some debug info is also deleted. This implementation can be used as soon
        #       as the remaining problems with the debug_tree are fixed.
        # Delete the variables that are no longer needed:
        # scoped_names = recordStore.get_names_current_scope()
        # for name in scoped_names:
        #     del recordStore[name]
        #     del generalStore[name]

        return self.crawled_data


def crawler_main(crawled_directory_path: str,
                 cfood_file_name: str,
                 identifiables_definition_file: str = None,
                 debug: bool = False,
                 provenance_file: str = None,
                 dry_run: bool = False,
                 prefix: str = "",
                 securityMode: SecurityMode = SecurityMode.UPDATE,
                 unique_names=True,
                 ):
    """

    Parameters
    ----------
    crawled_directory_path : str
        path to be crawled
    cfood_file_name : str
        filename of the cfood to be used
    identifiables_definition_file : str
        filename of an identifiable definition yaml file
    debug : bool
        whether or not to run in debug mode
    provenance_file : str
        provenance information will be stored in a file with given filename
    dry_run : bool
        do not commit any chnages to the server
    prefix : str
        remove the given prefix from file paths
    securityMode : int
        securityMode of Crawler
    unique_names : bool
        whether or not to update or insert entities inspite of name conflicts

    Returns
    -------
    return_value : int
        0 if successful
    """
    crawler = Crawler(debug=debug, securityMode=securityMode)
    try:
        crawler.crawl_directory(crawled_directory_path, cfood_file_name)
    except ConverterValidationError as err:
        print(err)
        return 1
    if provenance_file is not None:
        crawler.save_debug_data(provenance_file)

    if identifiables_definition_file is not None:

        ident = CaosDBIdentifiableAdapter()
        ident.load_from_yaml_definition(identifiables_definition_file)
        crawler.identifiableAdapter = ident

    if dry_run:
        ins, upd = crawler.synchronize(commit_changes=False)
        inserts = [str(i) for i in ins]
        updates = [str(i) for i in upd]
        with open("dry.yml", "w") as f:
            f.write(yaml.dump({
                "insert": inserts,
                "update": updates}))
    else:
        rtsfinder = dict()
        for elem in crawler.crawled_data:
            if isinstance(elem, db.File):
                # correct the file path:
                # elem.file = os.path.join(args.path, elem.file)
                if prefix is None:
                    raise RuntimeError(
                        "No prefix set. Prefix must be set if files are used.")
                if elem.path.startswith(prefix):
                    elem.path = elem.path[len(prefix):]
                elem.file = None
                # TODO: as long as the new file backend is not finished
                #       we are using the loadFiles function to insert symlinks.
                #       Therefore, I am setting the files to None here.
                #       Otherwise, the symlinks in the database would be replaced
                #       by uploads of the files which we currently do not want to happen.

            # Check whether all needed RecordTypes exist:
            if len(elem.parents) > 0:
                for parent in elem.parents:
                    if parent.name in rtsfinder:
                        continue

                    rt = db.RecordType(name=parent.name)
                    try:
                        rt.retrieve()
                        rtsfinder[parent.name] = True
                    except db.TransactionError:
                        rtsfinder[parent.name] = False
        notfound = [k for k, v in rtsfinder.items() if not v]
        if len(notfound) > 0:
            raise RuntimeError("Missing RecordTypes: {}".
                               format(", ".join(notfound)))

        crawler.synchronize(commit_changes=True, unique_names=unique_names)
    return 0


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=RawTextHelpFormatter)
    parser.add_argument("cfood_file_name",
                        help="Path name of the cfood yaml file to be used.")
    parser.add_argument("--provenance", required=False,
                        help="Path name of the provenance yaml file. "
                        "This file will only be generated if this option is set.")
    parser.add_argument("--debug", required=False, action="store_true",
                        help="Path name of the cfood yaml file to be used.")
    parser.add_argument("crawled_directory_path",
                        help="The subtree of files below the given path will "
                        "be considered. Use '/' for everything.")
    parser.add_argument("-c", "--add-cwd-to-path", action="store_true",
                        help="If given, the current working directory(cwd) is added to the Python "
                        "path.")
    parser.add_argument("-s", "--security-mode", choices=["retrieve", "insert", "update"],
                        default="retrieve",
                        help="Determines whether entities may only be read from the server, or "
                        "whether inserts or even updates may be done.")
    parser.add_argument("-n", "--dry-run", action="store_true",
                        help="Create two files dry.yml to show"
                        "what would actually be committed without doing the synchronization.")

    # TODO: load identifiables is a dirty implementation currently
    parser.add_argument("-i", "--load-identifiables",
                        help="Load identifiables from the given yaml file.")
    parser.add_argument("-u", "--unique-names",
                        help="Insert or updates entities even if name conflicts exist.")
    parser.add_argument("-p", "--prefix",
                        help="Remove the given prefix from the paths "
                        "of all file objects.")

    return parser.parse_args()


def main():
    args = parse_args()

    conlogger = logging.getLogger("connection")
    conlogger.setLevel(level=logging.ERROR)

    # logging config for local execution
    logger.addHandler(logging.StreamHandler(sys.stdout))
    if args.debug:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)

    if args.add_cwd_to_path:
        sys.path.append(os.path.abspath("."))
    sys.exit(crawler_main(
        crawled_directory_path=args.crawled_directory_path,
        cfood_file_name=args.cfood_file_name,
        identifiables_definition_file=args.load_identifiables,
        debug=args.debug,
        provenance_file=args.provenance,
        dry_run=args.dry_run,
        prefix=args.prefix,
        securityMode={"retrieve": SecurityMode.RETRIEVE,
                      "insert": SecurityMode.INSERT,
                      "update": SecurityMode.UPDATE}[args.security_mode],
        unique_names=args.unique_names,
    ))


if __name__ == "__main__":
    main()
