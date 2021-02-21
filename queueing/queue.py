from multiprocessing import SimpleQueue


class Queue:
    def __init__(self):
        self.queue = SimpleQueue()

    def enqueue(self, e):
        self.queue.put(e)

    def dequeue(self):
        return self.queue.get()

    def __len__(self):
        return self.queue.empty()
