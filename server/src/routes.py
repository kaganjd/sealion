import aiohttp
import json
from aiohttp import web
from scapy.all import *
import threading
import asyncio
import utils
from utils import get_interface, get_sniffer_config, start_loop, enqueue_packets, dequeue_packets, get_arp_table, arp_spoof, sniff_spoofed

utils.init()

def setup_routes(app):
    app.router.add_get('/sniff', sniff_handler),
    app.router.add_get('/main', main_handler)

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
                json_msg_data = json.loads(msg.data)
                arp_spoof(json_msg_data)
                neighbor_ip = json_msg_data['args']['ifaddr']
                new_loop = asyncio.new_event_loop()
                asyncio.run_coroutine_threadsafe(dequeue_packets(ws), new_loop)
                threading.Thread(target=start_loop, args=(new_loop,)).start()
                threading.Thread(target=sniff_spoofed(neighbor_ip)).start()
                # f.setDaemon(true)
            elif json_msg['fname'] == 'sniffSelf':
                print('Starting self sniff')
                json_msg_data = json.loads(msg.data)
                config = get_sniffer_config(json_msg_data['args'])
                new_loop = asyncio.new_event_loop()
                asyncio.run_coroutine_threadsafe(dequeue_packets(ws), new_loop)
                threading.Thread(target=start_loop, args=(new_loop,)).start()
                threading.Thread(target=enqueue_packets(config)).start()
                # f.setDaemon(true)
        elif msg.type == aiohttp.WSMsgType.ERROR:
            print('ws connection closed with exception %s' % ws.exception())
    print('websocket connection closed')
    return ws
