import aiohttp
from aiohttp import web
from scapy.all import *
import threading
import asyncio
import utils
from utils import get_interface, get_sniffer_config, start_loop, enqueue_packets, dequeue_packets

utils.init()

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
                new_loop = asyncio.new_event_loop()
                asyncio.run_coroutine_threadsafe(dequeue_packets(ws), new_loop)
                threading.Thread(target=start_loop, args=(new_loop,)).start()
                threading.Thread(target=enqueue_packets(config=config)).start()
        elif msg.type == aiohttp.WSMsgType.ERROR:
            print('ws connection closed with exception %s' %
                  ws.exception())
    print('websocket connection closed')
    return ws
