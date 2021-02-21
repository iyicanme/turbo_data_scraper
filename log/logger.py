from multiprocessing import Process
from time import strftime

from colorama import init, Fore


class Logger:
    def __init__(self, source):
        init(autoreset=True)

        self.source = source
        self.process = None

    def start(self):
        self.process = Process(target=self._work)
        self.process.start()

        return self

    def _work(self):
        while True:
            log_message = self.source.dequeue()

            if log_message is None:
                continue

            print(log_message)

    def join(self):
        self.process.join()

    @staticmethod
    def _get_time():
        return strftime("%d.%m.%Y %H:%M:%S")

    @staticmethod
    def s(log_queue, message):
        log_queue.enqueue("{} {} {}".format(Fore.GREEN, Logger._get_time(), message))

    @staticmethod
    def e(log_queue, message):
        log_queue.enqueue("{} {} {}".format(Fore.RED, Logger._get_time(), message))

    @staticmethod
    def i(log_queue, message):
        log_queue.enqueue("{} {} {}".format(Fore.WHITE, Logger._get_time(), message))

    @staticmethod
    def w(log_queue, message):
        log_queue.enqueue("{} {} {}".format(Fore.MAGENTA, Logger._get_time(), message))
