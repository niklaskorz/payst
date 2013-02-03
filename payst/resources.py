from __future__ import absolute_import, print_function
from flask.ext import restful
from flask.ext.restful import reqparse
from . import models
from .template import Template
import pygments
import pygments.lexers
import pygments.formatters
import pygments.util
import flask


class Index(restful.Resource):
    def render_html(data, code, headers=None):
        template_data = {
            "data": data,
            "headers": headers
        }
        resp = flask.make_response(Template("index.html").render(template_data), code)
        resp.headers.extend(headers or {})
        return resp

    representations = {
        "text/html": render_html
    }

    def get(self):
        return "Index"


def highlight_code(lang, code):
    try:
        lexer = pygments.lexers.get_lexer_by_name(lang, stripall=True)
    except pygments.util.ClassNotFound:
        lexer = pygments.lexers.get_lexer_by_name("text", stripall=True)
    formatter = pygments.formatters.HtmlFormatter(linenos=True, cssclass="syntax")
    return pygments.highlight(code, lexer, formatter)


class Pastes(restful.Resource):
    def render_html(data, code, headers=None):
        template_data = {
            "data": data,
            "headers": headers
        }
        resp = flask.make_response(Template("paste_created.html").render(template_data), code)
        resp.headers.extend(headers or {})
        return resp

    representations = {
        "text/html": render_html
    }

    reqparser = reqparse.RequestParser()
    reqparser.add_argument("name", type=str, location='form')
    reqparser.add_argument("description", type=str, location='form')
    reqparser.add_argument("lang", type=str, location='form')
    reqparser.add_argument("code", type=str, location='form')

    def post(self):
        args = self.reqparser.parse_args()
        paste = models.Paste(
            args["name"] or "",
            args["description"] or "",
            args["lang"] or "text",
            args["code"] or "")
        paste.save()
        data = {
            "status": 201,
            "message": "Created paste",
            "location": "/pastes/" + paste.id
        }
        return data, 201, {"Location": "/pastes/" + paste.id}


class Paste(restful.Resource):
    def render_html(data, code, headers=None):
        template_data = {
            "data": data,
            "headers": headers
        }
        resp = flask.make_response(Template("paste.html").render(template_data), code)
        resp.headers.extend(headers or {})
        return resp

    representations = {
        "text/html": render_html
    }

    def get(self, paste_id):
        try:
            paste = models.Paste.get(paste_id)
        except models.NotFoundException:
            flask.abort(404)
        data = {
            "id": paste.id,
            "name": paste.name,
            "description": paste.description,
            "lang": paste.lang,
            "code": paste.code,
            "highlighted_code": highlight_code(paste.lang, paste.code)
        }
        return data
