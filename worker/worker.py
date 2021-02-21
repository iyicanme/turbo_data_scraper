from abc import ABC, abstractmethod

from multiprocessing import Process


class Worker(ABC):
    def __init__(self, api, key, sleep_duration, log_queue):
        self.api = api
        self.key = key
        self.sleep_duration = sleep_duration
        self.log_queue = log_queue

        self.process = None

    def start(self):
        self.process = Process(target=self._work)
        self.process.start()

        return self

    def join(self):
        if self.process is not None:
            self.process.join()

    @abstractmethod
    def _work(self):
        pass
