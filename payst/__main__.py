from meinheld import server
from payst.app import app

server.listen(("0.0.0.0", 8000))
server.run(app)
