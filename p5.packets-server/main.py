from aiohttp import web
from routes import setup_routes
from middleware import cors_factory

app = web.Application(middlewares=[cors_factory])
setup_routes(app)
web.run_app(app)
