from __future__ import absolute_import, print_function
from meinheld import server
from .app import app

server.listen(("0.0.0.0", 8000))
server.run(app)
