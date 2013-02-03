from __future__ import absolute_import, print_function
from . import data
from .data import NotFoundException
import uuid


class Paste(object):
    def __init__(self, name, description, lang, code, _id=None):
        self.name = name
        self.description = description
        self.lang = lang
        self.code = code
        self.id = _id if _id is not None else uuid.uuid4().hex

    def save(self):
        paste = {
            "name": self.name,
            "description": self.description,
            "lang": self.lang,
            "code": self.code
        }
        data.paste_cf.insert(self.id, paste)

    def remove(self):
        data.paste_cf.remove(self._id)

    @classmethod
    def get(cls, _id):
        paste = data.paste_cf.get(_id)
        return cls(_id=_id, **paste)
