#!/usr/bin/env python
"""
NIMH Data Archive Data Structure Client

Example:
    nimh_data_archive -d demof01 child_dem01

"""
__author__ = 'Nolan Nichols <https://orcid.org/0000-0003-1099-3328>'

import os
import sys
import json
import logging

import requests


class DataDictionary(object):
    """Creates an object to retrieve NDA data dictionary.
    """
    def __init__(self, url):
        self.base_url = url
        self.datastructures_url = None
        self.request = requests.get(self.base_url)
        self.json = self.request.json()
        self.name = self.json.get('name')
        self.version = self.json.get('version')
        self.description = self.json.get('description')
        self.operations = self.json.get('operations')
        self.data_structures = dict()

    def get_data_sructures(self):
        self.datastructures_url = '{0}/datastructure'.format(self.base_url)
        request = requests.get(self.datastructures_url)
        data = request.json()
        for ds in data:
            self.data_structures.update({
                ds.get('shortName'): DataStructure(ds, self.base_url)})


class DataStructure(object):
    """Parses a Data Structure and corresponding data elements."""
    def __init__(self, data, url):
        self.category = data.get('category')
        self.data_type = data.get('dataType')
        self.ndar_url = data.get('ndarURL')
        self.publish_date = data.get('publishDate')
        self.short_name = data.get('shortName')
        self.source = data.get('source')
        self.status = data.get('status')
        self.title = data.get('title')
        self.json = dict()
        self.url = url
        self.data = data
        self.data_elements = None

    def get_data_elements(self):
        """Parses the data elements into a well-structured dictionary."""
        ds_url = '{0}/datastructure/{1}'.format(self.url, self.short_name)
        request = requests.get(ds_url)
        self.json.update(request.json())
        result = dict()
        for de in self.json.get('dataElements'):
            result.update({de.get('name'): DataElement(de)})
        self.data_elements = result


class DataElement(object):
    """Parses each data element including semi-structured content embedded as
    json strings."""
    def __init__(self, data):
        self.data = data
        self.required = data.get('required')
        self.aliases = data.get('aliases')
        self.position = data.get('position')
        self.name = data.get('name')
        self.type = data.get('type')
        self.description = data.get('description')
        self.title = data.get('title')
        if self.data.get('notes'):
            self.parse_notes()
        if self.data.get('valueRange'):
            self.value_range = self.parse_value_range()

    def parse_notes(self):
        """Parses the notes field, attempting to clean up coded values by
        adding a new "valueset" key to the dictionary."""
        notes = self.data.get('notes')
        codelist = notes.split(";")
        valueset = list()
        for codes in codelist:
            values = codes.split("=", 1)
            if (len(values) > 1) and not (self.data.get('notes') == "null"):
                self.data.update({'notes': ""})
            if len(values) > 1:
                result = dict()
                result.update({'code': values[0].strip()})
                result.update({'label': values[1].strip()})
                valueset.append(result)
            else:
                self.data.update({'notes': values[0]})
        self.data.update({'valueset': valueset})

    def parse_value_range(self):
        return self.data.get('valueRange')


def main(args=None):
    api = 'https://ndar.nih.gov/api/datadictionary/v2'
    data_dict = DataDictionary(api)
    data_dict.get_data_sructures()
    results = []
    for i in args.data_structures:
        data_structure = data_dict.data_structures.get(i)
        data_structure.get_data_elements()
        results.append(data_structure.json)
    for i in results:
        print(json.dumps(i))


if __name__ == "__main__":
    import argparse

    formatter = argparse.RawDescriptionHelpFormatter
    default = 'default: %(default)s'
    parser = argparse.ArgumentParser(prog="datastructure.py",
                                     description=__doc__,
                                     formatter_class=formatter)
    parser.add_argument('-d', '--data-structures',
                        nargs='*',
                        help="List of 1 of more data structures to download.")
    args = parser.parse_args()
    sys.exit(main(args=args))
