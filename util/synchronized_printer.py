from multiprocessing import Lock

from util.singleton import Singleton


class SynchronizedPrinter(metaclass=Singleton):
    def __init__(self):
        self.lock = Lock()

    def print_synchronized(self, message):
        with self.lock:
            print(message + "\n", end="")
