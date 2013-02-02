from flask import Flask, make_response
from flask.ext import restful
from payst import resources
from payst.view import View
import json

DEBUG=True
app = Flask(__name__)
app.config.from_object(__name__)
api = restful.Api(app)

api.add_resource(resources.Index, "/")
api.add_resource(resources.Pastes, "/pastes")
api.add_resource(resources.Paste, "/pastes/<string:paste_id>")

@api.representation("application/json")
def output_json(data, code, headers=None):
    if type(data) == View:
        resp = make_response(data.render("json"), code)
    elif type(data) == dict:
        resp = make_response(json.dumps(data), code)
    else:
        resp = make_response(str(data), code)
    resp.headers.extend(headers or {})
    return resp

@api.representation("text/html")
def output_html(data, code, headers=None):
    if type(data) == View:
        resp = make_response(data.render("html"), code)
    elif type(data) == dict:
        resp = make_response(json.dumps(data), code)
    else:
        resp = make_response(str(data), code)
    resp.headers.extend(headers or {})
    return resp
