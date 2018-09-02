import aiohttp
from aiohttp import web
from scapy.all import *

async def index(request):
    return web.Response(text='hello')

async def websocket_handler(request):

    p = IP(dst="github.com")/TCP()
    r = sr1(p)
    resp = r.summary()

    ws = web.WebSocketResponse()
    await ws.prepare(request)

    async for msg in ws:
        if msg.type == aiohttp.WSMsgType.TEXT:
            if msg.data == 'close':
                await ws.close()
            else:
                await ws.send_str(resp + '/answer')
        elif msg.type == aiohttp.WSMsgType.ERROR:
            print('ws connection closed with exception %s' %
                  ws.exception())

    print('websocket connection closed')

    return ws
