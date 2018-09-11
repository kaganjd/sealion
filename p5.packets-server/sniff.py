from scapy.all import *
import argparse
import sys

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

def get_sniffer_config(args=''):
    config = {
        'count': 5,
        'filter': '',
        'iface': conf.iface,
        'lfilter': '',
        'prn': lambda x: x.summary(),
        'store': 0
    }

    try:
        count = args.get('count')
        if count is None:
            count = config['count']
        else:
            config.update(count=count)
    except AttributeError:
        print('hork')

    try:
        filter = args.get('filter')
        if filter is None:
            filter = config['filter']
        else:
            config.update(filter=filter)
    except AttributeError:
        print('hork')

    try:
        iface = args.get('iface')
        if iface is None:
            iface = config['iface']
        else:
            config.update(iface=iface)
    except AttributeError:
        print('hork')

    try:
        lfilter = args.get('lfilter')
        if lfilter is None:
            lfilter = config['lfilter']
        else:
            config.update(lfilter=lfilter)
    except AttributeError:
        print('hork')

    try:
        prn = args.get('prn')
        if prn is None:
            prn = config['prn']
        else:
            config.update(prn=prn)
    except AttributeError:
        print('hork')

    try:
        store = args.get('store')
        if store is None:
            store = config['store']
        else:
            config.update(store=store)
    except AttributeError:
        print('hork')

    return config

get_interface()
sniff(**get_sniffer_config())
