from abc import ABC, abstractmethod

from multiprocessing import Process


class Worker(ABC):
    def __init__(self, api, key):
        self.api = api
        self.key = key

    def start(self):
        p = Process(target=self._work)
        p.start()

    @abstractmethod
    def _work(self):
        pass
