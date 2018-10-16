import aiohttp
import json
from aiohttp import web
from scapy.all import *
from sniff import get_interface
import threading

q = Queue()

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
                config = get_sniffer_config(passed_config=msg.data)
                threading.Thread(target=read_q).start()
                threading.Thread(target=sniff_process(config=config)).start()
                await ws.send_str('hello')
        elif msg.type == aiohttp.WSMsgType.ERROR:
            print('ws connection closed with exception %s' %
                  ws.exception())
    print('websocket connection closed')
    return ws

def get_sniffer_config(**kwargs):
    default_config = {
        "count": 5,
        "filter": "",
        "iface": conf.iface,
        "lfilter": "",
        "store": 0
    }

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

def sniff_process(**kwargs):
    k = kwargs['config']
    def summarize(x):
        logger = 1
        pkt_summary = x.summary()
        print('{}--{}'.format(logger, pkt_summary))
        q.put('{}--{}'.format(logger, pkt_summary))
    sniff(**k, prn=lambda x: summarize(x))

def read_q():
    while True:
        logger = 2
        pkt_summary = q.get()
        if pkt_summary:
            print('{}--{}'.format(logger, pkt_summary))
