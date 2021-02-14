from time import strftime

from colorama import init, Fore


class Log:
    def __init__(self):
        init(autoreset=True)

    @staticmethod
    def _get_time():
        return strftime("%d.%m.%Y %H:%M:%S")

    @staticmethod
    def e(message):
        print(Fore.RED, Log._get_time(), message)

    @staticmethod
    def i(message):
        print(Fore.WHITE, Log._get_time(), message)

    @staticmethod
    def s(message):
        print(Fore.GREEN, Log._get_time(), message)

    @staticmethod
    def w(message):
        print(Fore.MAGENTA, Log._get_time(), message)
