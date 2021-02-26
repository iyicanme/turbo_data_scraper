from abc import ABC, abstractmethod

from multiprocessing import Process


class Worker(ABC):
    def __init__(self):
        self.keep_running = True
        self.process = None

    def start(self):
        self.process = Process(target=self._work)
        self.process.start()

        return self

    def join(self):
        if self.process is not None:
            self.process.join()

    def signal_termination(self):
        self.keep_running = False

    @abstractmethod
    def _work(self):
        pass
