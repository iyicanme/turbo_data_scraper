from abc import ABC, abstractmethod


class Sink(ABC):
    @abstractmethod
    def write(self, data):
        pass

    @abstractmethod
    def close(self):
        pass
