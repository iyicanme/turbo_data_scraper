from multiprocessing import SimpleQueue, Lock


class IdQueue:
    def __init__(self):
        self.queue = SimpleQueue()
        self.lock = Lock()

    def enqueue(self, e):
        self.queue.put(e)

    def dequeue(self):
        return self.queue.get()

    def __len__(self):
        return self.queue.empty()
