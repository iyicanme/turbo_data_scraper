from queuing.fifo import Fifo


class Broker:
    def __init__(self):
        self.queue_count = 0
        self.queues = []

        self.sequence = 0

    def create_queue(self):
        queue = Fifo()

        self.queues.append(queue)
        self.queue_count += 1

        return queue

    def dequeue(self):
        queue_index = self.sequence

        self.sequence += 1
        self.sequence %= self.queue_count

        return self.queues[queue_index].dequeue()

    def get_contents(self):
        queue_contents = []

        for queue in self.queues:
            queue_contents.extend(queue)

        return queue_contents
