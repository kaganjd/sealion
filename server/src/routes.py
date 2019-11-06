import aiohttp
import json
from aiohttp import web
from scapy.all import *
import threading
import asyncio
from utils.sniff_module import Sniffer
from utils.network_info import get_interface, get_arp_table, arp_spoof

def setup_routes(app):
    app.router.add_get('/sniff', sniff_handler),
    app.router.add_get('/main', main_handler)

async def main_handler(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)
    try:
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
                    json_arp_table = json.dumps(get_arp_table(json_msg['args']['  ifaddr']))
                    await ws.send_str(json_arp_table)
            elif msg.type == aiohttp.WSMsgType.ERROR:
                print('ws connection closed with exception %s' % ws.exception())
    except Exception as e:
        print('Main error: ', e)
        await ws.close()
    print('Main websocket connection closed')
    return ws

async def sniff_handler(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)
    try:
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
                    s = Sniffer(ws, json_msg['fname'], neighbor_ip)
                    s.start_sniff_threads()
                elif json_msg['fname'] == 'sniffSelf':
                    print('Starting self sniff')
                    s = Sniffer(ws, json_msg['fname'])
                    s.start_sniff_threads()
            elif msg.type == aiohttp.WSMsgType.ERROR:
                print('ws connection closed with exception %s' % ws.exception())
    except Exception as e:
        print('Sniff error: ', e)
        await ws.close()
    print('Sniff websocket connection closed')
    return ws
