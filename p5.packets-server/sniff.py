from scapy.all import *
from scapy.arch.unix import read_routes
import argparse

a = read_routes() # only for unix
interface_info = {
    'gw': a[0][2],
    'netif': a[0][3],
    'ifaddr': a[0][4],
}
print('interface_info: ', interface_info)

parser = argparse.ArgumentParser()
parser.add_argument("--count", help="The number of packets to sniff (integer). 0 (default) is indefinite count.")
parser.add_argument("--filter", help="BPF filter to apply")
parser.add_argument("--iface", help="The network interface to sniff on.")
parser.add_argument("--prn", help="Function to apply to each packet.")
parser.add_argument("--lfilter", help="Function to apply to each packet. Should be a filter check.")
args = parser.parse_args()
if args.count:
    try:
        count = int(args.count)
        print("Sniffing %d packets." % count)
    except: 
        print("Count is not a valid integer, using default of 5. Ctrl + C to stop sending packets.")
        count = 5
else:
    count = 5
    print("Using default packet count of 5. Ctrl + C to stop sending packets.")

if args.filter:
    filter = args.filter
else: 
    filter = ""

if args.iface:
    iface = args.iface
else: 
    iface = conf.iface

if args.prn:
    prn = args.prn
else: 
    prn = lambda x: x.summary()

if args.lfilter:
    lfilter = args.lfilter
else:
    lfilter  = ""

sniff(filter=filter, prn=prn, count=count, lfilter=lfilter, iface=iface, store=0)
