from __future__ import absolute_import, print_function
from flask import Flask, make_response
from flask.ext import restful
from . import resources
from .template import Template
import json

app = Flask(__name__)
app.debug = True
api = restful.Api(app)

api.add_resource(resources.Index, "/")
api.add_resource(resources.Pastes, "/pastes")
api.add_resource(resources.Paste, "/pastes/<string:paste_id>")

@api.representation("text/html")
def output_html(data, code, headers=None):
    template_data = {
        "data": data,
        "headers": headers
    }
    try:
        template = Template("error/{0}.html".format(code))
        resp = make_response(template.render(template_data), code)
    except IOError:
        try:
            template = Template("error/default.html")
            resp = make_response(template.render(template_data), code)
        except IOError:
            resp = make_response(json.dumps(data), code)
    resp.headers.extend(headers or {})
    return resp
