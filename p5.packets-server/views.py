import aiohttp
from aiohttp import web
from scapy.all import *
import threading
import asyncio
import utils
from utils import get_interface, get_sniffer_config, start_loop, enqueue_packets, dequeue_packets, get_arp_table, arp_spoof, sniff_spoofed

utils.init()

# async def serve_interface(request):
#     return web.json_response(get_interface())

async def sniff_arp_handler(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)
    async for msg in ws:
        if msg.type == aiohttp.WSMsgType.TEXT:
            json_msg = aiohttp.WSMessage.json(msg)
            if json_msg['fname'] == 'stopSniffer':
                print('Stopping sniffer')
                await ws.close()
            elif json_msg['fname'] == 'getNetworkInfo':
                print('Getting network info')
                await ws.send_str(get_interface())
            elif json_msg['fname'] == 'arpScan':
                arp_table = get_arp_table(json_msg['args']['ifaddr'])
                await ws.send_str(arp_table)
            elif json_msg['fname'] == 'sniffNeighbor':
                import json
                print('Starting neighbor sniff')
                json_msg_data = json.loads(msg.data)
                neighbor_ip = json_msg_data['args']['ifaddr']
                new_loop = asyncio.new_event_loop()
                asyncio.run_coroutine_threadsafe(sniff_spoofed(neighbor_ip), new_loop)
                threading.Thread(target=start_loop, args=(new_loop,)).start()
                threading.Thread(target=arp_spoof(json_msg_data)).start()
            elif json_msg['fname'] == 'sniffSelf':
                print('Starting self sniff')
                config = get_sniffer_config(msg.data)
                new_loop = asyncio.new_event_loop()
                asyncio.run_coroutine_threadsafe(dequeue_packets(ws), new_loop)
                threading.Thread(target=start_loop, args=(new_loop,)).start()
                threading.Thread(target=enqueue_packets(config)).start()
        elif msg.type == aiohttp.WSMsgType.ERROR:
            print('ws connection closed with exception %s' % ws.exception())
    print('websocket connection closed')
    return ws
