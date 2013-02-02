from flask.ext import restful
from flask.ext.restful import reqparse
from payst import models
from payst.view import View
import pygments
import pygments.lexers
import pygments.formatters
import pygments.util

def highlight_code(lang, code):
    try:
        lexer = pygments.lexers.get_lexer_by_name(lang, stripall=True)
    except pygments.util.ClassNotFound:
        lexer = pygments.lexers.get_lexer_by_name("text", stripall=True)
    formatter = pygments.formatters.HtmlFormatter(linenos=True, cssclass="syntax")
    return pygments.highlight(code, lexer, formatter)


class Index(restful.Resource):
    def get(self):
        return View("index", {})


class Pastes(restful.Resource):
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
        return View("paste", {
            "paste": {
                "id": paste.id,
                "name": paste.name,
                "description": paste.description,
                "lang": paste.lang,
                "code": paste.code,
                "highlighted_code": highlight_code(paste.lang, paste.code)
            }
        }), 303, {"Location": "/pastes/" + paste.id}


class Paste(restful.Resource):
    def get(self, paste_id):
        paste = models.Paste.get(paste_id)
        if paste is None:
            return None, 404
        return View("paste", {
            "paste": {
                "id": paste.id,
                "name": paste.name,
                "description": paste.description,
                "lang": paste.lang,
                "code": paste.code,
                "highlighted_code": highlight_code(paste.lang, paste.code)
            }
        })
