#!/usr/bin/env python
"""
============================
RDoCdb Data Structure Client
============================

"""
__author__ = 'Nolan Nichols <https://orcid.org/0000-0003-1099-3328>'

import os
import sys

import requests


class Connection(object):
    def __init__(self, url):
        self.url = url
        self.request = requests.get(self.url)

    def __repr__(self):
        return "{0}:{1}".format(self.__class__, self.name)


class DataDictionary(Connection):
    def __init__(self, url):
        super(DataDictionary, self).__init__(url)
        self.json = self.request.json()
        self.name = self.json.get('name')
        self.version = self.json.get('version')
        self.description = self.json.get('description')
        self.operations = self.json.get('operations')

    def __repr__(self):
        return "{0}:{1}".format(self.__class__, self.name)

    def get_data_sructures(self):
        ds_url = '{0}/datastructure'.format(self.url)
        request = requests.get(ds_url)
        data = request.json()
        result = dict()
        for ds in data:
            result.update({ds.get('shortName'): DataStructure(ds, self.url)})
        return result


class DataStructure(object):
    def __init__(self, data, url):
        self.category = data.get('category')
        self.data_type = data.get('dataType')
        self.ndar_url = data.get('ndarURL')
        self.publish_date = data.get('publishDate')
        self.short_name = data.get('shortName')
        self.source = data.get('source')
        self.status = data.get('status')
        self.title = data.get('title')
        self.url = url

    def __repr__(self):
        return "{0}:{1}".format(self.__class__, self.short_name)

    def get_data_elements(self):
        ds_url = '{0}/datastructure/{1}'.format(self.url, self.short_name)
        request = requests.get(ds_url)
        data = request.json()
        result = dict()
        for de in data.get('dataElements'):
            result.update({de.get('name'): DataElement(de)})
        return result


class DataElement(object):
    def __init__(self, data):
        self.required = data.get('required')
        self.aliases = data.get('aliases')
        self.position = data.get('position')
        self.name = data.get('name')
        self.type = data.get('type')
        self.description = data.get('description')
        self.value_range = data.get('valueRange')
        self.title = data.get('title')

    def __repr__(self):
        return "{0}:{1}".format(self.__class__, self.name)

def main(args=None):
    pass


if __name__ == "__main__":
    import argparse

    formatter = argparse.RawDescriptionHelpFormatter
    default = 'default: %(default)s'
    parser = argparse.ArgumentParser(prog="datastructure.py",
                                     description=__doc__,
                                     formatter_class=formatter)
    args = parser.parse_args()
    sys.exit(main(args=args))