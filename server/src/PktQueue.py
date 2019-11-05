import queue

# https://stackoverflow.com/questions/48705408/sharing-a-queue-instance-between-different-modules
class _QueueProxy(object):
    def __init__(self):
        self._queue = queue.Queue(maxsize=50)
        self.qsize = self._queue.qsize()

    def get(self, *args, **kw):
        return self._queue.get(*args, **kw)

    def put(self, *args, **kw):
        return self._queue.put(*args, **kw)
   
shared_queue = _QueueProxy()
