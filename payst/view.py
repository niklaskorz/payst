import pystache
import json
import os.path
import sys

class View(object):
    def __init__(self, template, data):
        self.template = template
        self.data = data

    def render(self, format):
        template_path = "templates/{0}.{1}".format(self.template, format)
        if os.path.isfile(template_path):
            with open(template_path) as f:
                return pystache.render(f.read(), self.data)
        else:
            return json.dumps(self.data)
