import aiohttp
from aiohttp import web
from scapy.all import *
from sniff import get_interface

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
                print(msg.data)
                await ws.send_str('message from server')
        elif msg.type == aiohttp.WSMsgType.ERROR:
            print('ws connection closed with exception %s' %
                  ws.exception())
    print('websocket connection closed')
    return ws

