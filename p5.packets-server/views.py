import aiohttp
from aiohttp import web
from scapy.all import *
import threading
import asyncio
import utils
from utils import get_interface, get_sniffer_config, start_loop, enqueue_packets, dequeue_packets, get_arp_table, get_neighbor_sniffer_config

utils.init()

async def serve_interface(request):
    return web.json_response(get_interface())

async def arp_scan(request):
    return web.json_response(get_arp_table(request.query))

async def sniffer_socket(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)
    
    async for msg in ws:
        if msg.type == aiohttp.WSMsgType.TEXT:
            if msg.data == 'stop':
                print('stopping sniffer')
                await ws.close()
            elif 'ifaddr' in msg.data:
                print('Starting neighbor sniff')
                config = get_neighbor_sniffer_config(msg.data)
            else:
                print('Starting self sniff')
                config = get_sniffer_config(msg.data)
                new_loop = asyncio.new_event_loop()
                asyncio.run_coroutine_threadsafe(dequeue_packets(ws), new_loop)
                threading.Thread(target=start_loop, args=(new_loop,)).start()
                threading.Thread(target=enqueue_packets(config=config)).start()
        elif msg.type == aiohttp.WSMsgType.ERROR:
            print('ws connection closed with exception %s' %
                  ws.exception())
    print('websocket connection closed')
    return ws
