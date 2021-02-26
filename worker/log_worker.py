from worker.worker import Worker


class LogWorker(Worker):
    def __init__(self, source):
        Worker.__init__(self)

        self.source = source

    def _work(self):
        while True:
            log_message = self.source.dequeue()

            if log_message is None:
                continue

            print(log_message)
