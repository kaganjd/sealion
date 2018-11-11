import json
from scapy.all import *
import asyncio
from urllib.parse import parse_qs, urlparse

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

def get_sniffer_config(config_from_client):
    default_config = {
        "count": 5,
        "filter": "",
        "iface": conf.iface,
        "lfilter": "",
        "store": 0
    }
    new_config = json.loads(config_from_client)
    for key in default_config:
        update_config(key, default_config, new_config)
    updated_config = default_config
    return updated_config

def get_neighbor_sniffer_config(config_from_client):
    new_config = json.loads(config_from_client)
    print(type(new_config))
    print(new_config)
    print(new_config['ifaddr'])

def update_config(key, default_config, new_config):
    try:
        if new_config.get(key) is not None:
            print('Updating "%s" in default_config' % key)
            new_val = new_config.get(key)
            default_config.update({key: new_val})
    # Not actually sure this error is possible anymore, but can be a placeholder depending on how we structure the config on the client side
    except AttributeError:
        print('No key "%s" in the args dict that was passed; using the default value' % key)

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

def get_arp_table(ifaddr):
    four_octets = ifaddr.get('ifaddr').split('.')
    del four_octets[-1]
    three_octets = '.'.join(four_octets)
    subnet = '{}{}'.format(three_octets, '.*')
    # http://redimp.de/posts/scapy-without-entering-promiscuous-mode/
    answered, unanswered = arping(subnet)
    hosts = [(host[1].hwsrc, host[1].psrc) for host in answered]
    return json.dumps(hosts)
