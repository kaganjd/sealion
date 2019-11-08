from scapy.all import *
import queue
import threading
import asyncio

# The queue proxy lets us initialize a queue once that is accessible by
# different objects
# More info: https://stackoverflow.com/questions/48705408/sharing-a-queue-instance-between-different-modules
class QueueProxy(object):
    def __init__(self):
        self._queue = queue.Queue(maxsize=50)
        self.qsize = self._queue.qsize()

    def get(self, *args, **kw):
        return self._queue.get(*args, **kw)

    def put(self, *args, **kw):
        return self._queue.put(*args, **kw)

# This is an implementation of Scapy's custom Session class that puts
# packets into the shared queue as they are sniffed.
# More info: https://scapy.readthedocs.io/en/latest/usage.html#asynchronous-sniffing
class EnqueueSession(DefaultSession):
    def __init__(self, *args, **kwargs):
        DefaultSession.__init__(self, *args, **kwargs)

    def on_packet_received(self, pkt):
        shared_queue.put(pkt.summary())
        DefaultSession.on_packet_received(self, pkt)

# This is an implementation of a stoppable thread, used in Sea Lion for
# dequeueing packets to send to the client. The threads needs to be stoppable
# so that when the websocket is closed from the client side, the dequeue
# thread can be properly killed, aside from the killing the websocket
# on the server side.
# More info: https://stackoverflow.com/questions/47912701/python-how-can-i-implement-a-stoppable-thread
class StoppableThread(threading.Thread):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._stop_event = threading.Event()

    def stop(self, *args, **kwargs):
        print('Stopping dequeue thread')
        self._stop_event.set()

    def stopped(self, *args, **kwargs):
        return self._stop_event.is_set()

# This is the Sniffer object that's instantiated with a websocket, function
# name, and optional target IP to sniff. The methods set up the threads for
# enqueueing and dequeueing packets from a shared queue.
class Sniffer(object):
    def __init__(self, ws, fname, ip=False):
        self.ws = ws
        self.fname = fname
        self.ip = ip

    def start_sniff_threads(self):
        self.sniff_thread()
        self.dequeue_thread()

    def sniff_thread(self):
        if self.fname == 'sniffSelf':
            AsyncSniffer(session=EnqueueSession).start()
        elif self.fname == 'sniffNeighbor':
            AsyncSniffer(
                session=EnqueueSession,
                filter='ip host {}'.format(self.ip)).start()

    async def send_dequeue_packets(self):
        while True:
            p = shared_queue.get()
            await self.ws.send_str(p)
            if self.ws.closed:
                threading.current_thread().stop()
                break

    # This is a helper function that starts a forever loop for the dequeue
    # function to run inside of.
    # More info: https://hackernoon.com/threaded-asynchronous-magic-and-how-to-wield-it-bba9ed602c32
    def start_loop(self, loop):
        asyncio.set_event_loop(loop)
        loop.run_forever()

    def dequeue_thread(self):
        new_loop = asyncio.new_event_loop()
        asyncio.run_coroutine_threadsafe(self.send_dequeue_packets(), new_loop)
        d = StoppableThread(target=self.start_loop, args=(new_loop, ))
        d.start()

# This the queue proxy that's shared between enqueue and dequeue functions.
# One function puts the packets in the queue; another function takes them
# out and sends them to the client.
shared_queue = QueueProxy()
