import threading
import asyncio

# https://stackoverflow.com/questions/47912701/python-how-can-i-implement-a-stoppable-thread
class DequeueThread(threading.Thread):
    def __init__(self, *args, **kwargs):
      super().__init__(*args, **kwargs)
      self._stop_event = threading.Event()

    def stop(self, *args, **kwargs):
      print('Stopping dequeue thread')
      self._stop_event.set()

    def stopped(self, *args, **kwargs):
      return self._stop_event.is_set()
