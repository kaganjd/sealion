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
