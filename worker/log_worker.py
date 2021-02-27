from worker.worker import Worker


class LogWorker(Worker):
    def __init__(self, source, dump_path):
        Worker.__init__(self)

        self.source = source
        self.dump_path = dump_path

    def _work(self):
        log_message = self.source.dequeue()

        if log_message is None:
            return

        print(log_message)

    def _cleanup(self):
        pending_logs = self.source.get_contents()

        for log in pending_logs:
            print(log)
