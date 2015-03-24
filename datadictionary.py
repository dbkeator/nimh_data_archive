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


class DataDictionary(object):
    def __init__(self, url):
        self.url = url
        self.request = requests.get(self.url)
        self.json = self.request.json()
        self.name = self.json['name']
        self.version = self.json['version']
        self.description = self.json['description']
        self.operations = self.json['operations']

    def __repr__(self):
        return self.name



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