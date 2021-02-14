from abc import ABC, abstractmethod

from multiprocessing import Process


class Worker(ABC):
    def __init__(self, api, key):
        self.api = api
        self.key = key
        self.process = None

    def start(self):
        self.process = Process(target=self._work)
        self.process.start()

    def join(self):
        if self.process is not None:
            self.process.join()

    @abstractmethod
    def _work(self):
        pass
