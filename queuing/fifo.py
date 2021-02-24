from multiprocessing import Queue

from queue import Empty


class Fifo:
    def __init__(self):
        self.queue = Queue()

    def enqueue(self, e):
        self.queue.put(e)

    def dequeue(self):
        try:
            return self.queue.get(block=False)
        except Empty:
            return None

    def __len__(self):
        return self.queue.empty()
