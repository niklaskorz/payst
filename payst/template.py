from __future__ import absolute_import, print_function
import pystache
import json
import os.path
import sys


class Template(object):
    def __init__(self, name):
        with open("templates/" + name) as f:
            self.template = f.read()

    def render(self, data):
        return pystache.render(self.template, data)
