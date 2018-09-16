from scapy.all import *
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

    def args_to_config(key):
        try:
            key = args.get(str(key))
            if key is None:
                key = config[str(key)]
            else:
                config.update(key=key)
        except AttributeError:
            print('No key "%s" in the args dict that was passed to get_sniffer_config' % key)
            print('Using the default value')

    for key in config:
        args_to_config(key)

    return config

# get_interface()
# sniff(**get_sniffer_config())
