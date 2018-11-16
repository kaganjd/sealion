from views import sniff_arp_handler

def setup_routes(app):
    app.router.add_get('/sniff', sniff_arp_handler),
