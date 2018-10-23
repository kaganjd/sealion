import json
from scapy.all import *
import asyncio

def init():
    global packet_queue
    packet_queue = Queue(maxsize=50)

def get_interface():
    # https://stackoverflow.com/questions/446209/possible-values-from-sys-platform
    if sys.platform == 'darwin':
        from scapy.arch.unix import read_routes
        a = read_routes()
        interface_info = {
            'gw': a[0][2],
            'netif': a[0][3],
            'ifaddr': a[0][4],
        }
        return interface_info

    elif sys.platform == 'linux2':
        from scapy.arch.linux import get_if_list
        interface_info = get_if_list()
        return interface_info

    elif sys.platform == 'win32':
        from scapy.arch.windows.__init__ import show_interfaces
        interface_info = show_interfaces()
        return interface_info

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

# from https://hackernoon.com/threaded-asynchronous-magic-and-how-to-wield-it-bba9ed602c32
def start_loop(loop):
    asyncio.set_event_loop(loop)
    loop.run_forever()

def enqueue_packets(**kwargs):
    k = kwargs['config']
    def summarize(x):
        logger = 1
        pkt_summary = x.summary()
        to_q = '{}--{}'.format(logger, pkt_summary)
        # print(to_q)
        packet_queue.put(to_q)
    sniff(**k, prn=lambda x: summarize(x))

async def dequeue_packets(ws):
    while True:
        logger = 2
        pkt_summary = packet_queue.get()
        if pkt_summary:
            from_q = '{}--{}'.format(logger, pkt_summary)
            # print(from_q)
            await ws.send_str(from_q)
