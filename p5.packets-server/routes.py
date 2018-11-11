from views import serve_interface, sniffer_socket, arp_scan

def setup_routes(app):
    app.router.add_get('/interface', serve_interface),
    app.router.add_get('/sniffer', sniffer_socket),
    app.router.add_get('/arp', arp_scan),
