from aiohttp import web
from routes import setup_routes
from permissions import *

check_permissions()
app = web.Application()
setup_routes(app)
web.run_app(app)
restore_permissions()
