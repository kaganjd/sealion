import aiohttp
import json
from aiohttp import web
from scapy.all import *
import threading
import asyncio
import utils
from utils import get_interface, start_loop, enqueue_packets, dequeue_packets, get_arp_table, arp_spoof

utils.init()

def setup_routes(app):
    app.router.add_get('/sniff', sniff_handler),
    app.router.add_get('/main', main_handler)

def call_sniff_threads(ws, fcn, ip=False):
  new_loop = asyncio.new_event_loop()
  asyncio.run_coroutine_threadsafe(dequeue_packets(ws), new_loop)
  threading.Thread(target=start_loop, args=(new_loop,)).start()
  threading.Thread(target=enqueue_packets(fcn, ip).start())

async def main_handler(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)
    async for msg in ws:
        if msg.type == aiohttp.WSMsgType.TEXT:
            json_msg = aiohttp.WSMessage.json(msg)
            if json_msg['fname'] == 'closeSocket':
                print('Closing socket')
                await ws.close()
            elif json_msg['fname'] == 'getNetworkInfo':
                print('Getting network info')
                json_iface = json.dumps(get_interface())
                await ws.send_str(json_iface)
            elif json_msg['fname'] == 'arpScan':
                json_arp_table = json.dumps(get_arp_table(json_msg['args']['ifaddr']))
                await ws.send_str(json_arp_table)
        elif msg.type == aiohttp.WSMsgType.ERROR:
            print('ws connection closed with exception %s' % ws.exception())
    print('websocket connection closed')
    return ws

async def sniff_handler(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)
    async for msg in ws:
        if msg.type == aiohttp.WSMsgType.TEXT:
            json_msg = aiohttp.WSMessage.json(msg)
            if json_msg['fname'] == 'closeSocket':
                print('Closing socket')
                await ws.close()
            elif json_msg['fname'] == 'sniffNeighbor':
                print('Starting neighbor sniff')
                neighbor_ip = json_msg['args']['ifaddr']
                arp_spoof(neighbor_ip)
                call_sniff_threads(ws, json_msg['fname'], neighbor_ip)
            elif json_msg['fname'] == 'sniffSelf':
                print('Starting self sniff')
                call_sniff_threads(ws, json_msg['fname'])
        elif msg.type == aiohttp.WSMsgType.ERROR:
            print('ws connection closed with exception %s' % ws.exception())
    print('websocket connection closed')
    return ws
