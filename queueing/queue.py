from multiprocessing import Queue as MpQueue


class Queue:
    def __init__(self):
        self.queue = MpQueue()

    def enqueue(self, e):
        self.queue.put(e)

    def dequeue(self):
        try:
            return self.queue.get(block=False)
        except Exception:
            return None

    def __len__(self):
        return self.queue.empty()
