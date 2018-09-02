from views import index, websocket_handler

def setup_routes(app):
    app.router.add_get('/', index)
    app.router.add_get('/payload', websocket_handler)
