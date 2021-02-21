from queueing.queue import Queue


class Dealer:
    def __init__(self):
        self.queue_count = 0
        self.queues = []

        self.sequence = 0

    def create_queue(self):
        queue = Queue()

        self.queues.append(queue)
        self.queue_count += 1

        return queue

    def enqueue(self, data):
        queue_index = self.sequence

        self.sequence += 1
        self.sequence %= self.queue_count

        self.queues[queue_index].enqueue(data)
