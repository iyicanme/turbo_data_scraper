from abc import ABC, abstractmethod


class Sink(ABC):
    def __init__(self):
        pass

    def __del__(self):
        pass

    @abstractmethod
    def write(self, data):
        pass
