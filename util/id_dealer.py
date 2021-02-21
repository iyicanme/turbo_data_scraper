from util.id_queue import IdQueue


class IdDealer:
    def __init__(self, worker_count):
        self.worker_count = worker_count
        self.worker_queues = []

        self.sequence = 0

        for i in range(worker_count):
            self.worker_queues.append(IdQueue())

    def get_queue(self, i):
        return self.worker_queues[i]

    def enqueue(self, data):
        queue_index = self.sequence

        self.sequence += 1
        self.sequence %= self.worker_count

        self.worker_queues[queue_index].enqueue(data)
