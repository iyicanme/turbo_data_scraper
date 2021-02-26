from abc import ABC

from worker.worker import Worker


class ApiWorker(Worker, ABC):
    def __init__(self, api, key, sleep_duration, log_queue):
        self.api = api
        self.key = key
        self.sleep_duration = sleep_duration
        self.log_queue = log_queue

        Worker.__init__(self)
