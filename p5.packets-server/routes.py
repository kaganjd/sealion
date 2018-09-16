from views import interface_socket

def setup_routes(app):
    app.router.add_get('/interfaces', interface_socket)
