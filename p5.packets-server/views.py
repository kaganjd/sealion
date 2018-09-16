import aiohttp
from aiohttp import web
from scapy.all import *
from sniff import get_interface

async def interface_socket(request):
    return web.json_response(get_interface())

