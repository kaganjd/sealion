import aiohttp
import json
from aiohttp import web
from scapy.all import *
from sniff import get_interface

pkt_array = []

async def serve_interface(request):
    return web.json_response(get_interface())

async def sniffer_socket(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)
    
    async for msg in ws:
        if msg.type == aiohttp.WSMsgType.TEXT:
            if msg.data == 'close':
                await ws.close()
            else:
                print('msg.data: %s' % msg.data)
                s = get_sniffer_config(passed_config=msg.data)
                sniff(**s)
                for pkt in pkt_array:
                    await ws.send_str(str(pkt))
        elif msg.type == aiohttp.WSMsgType.ERROR:
            print('ws connection closed with exception %s' %
                  ws.exception())
    print('websocket connection closed')
    return ws

def get_sniffer_config(**kwargs):
    default_config = {
        'count': 5,
        'filter': '',
        'iface': conf.iface,
        'lfilter': '',
        'prn': lambda x: send_packet(x),
        'store': 0
    }
    
    def send_packet(raw):
        pkt_array.append(raw)
        return

    def update_config(key):
        passed_config = json.loads(kwargs['passed_config'])
        try:
            if passed_config.get(key) is not None:
                print('Updating "%s" in default_config' % key)
                passed_val = passed_config.get(key)
                default_config.update({key: passed_val})
        # Not actually sure this error is possible anymore, but can be a placeholder depending on how we structure the config on the client side
        except AttributeError:
            print('No key "%s" in the args dict that was passed to get_sniffer_config; using the default value' % key)

    for key in default_config:
        update_config(key)

    return default_config
