from scapy.all import *
import PktQueue

class SLSession(DefaultSession):
  def __init__(self, *args, **kwargs):
    DefaultSession.__init__(self, *args, **kwargs)

  def on_packet_received(self, pkt):
    PktQueue.shared_queue.put(pkt.summary())
    DefaultSession.on_packet_received(self, pkt)
