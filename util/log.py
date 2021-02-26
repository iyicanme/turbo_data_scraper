from time import strftime

from colorama import init, Fore


def init_logging():
    init(autoreset=True)


def _get_time():
    return strftime("%d.%m.%Y %H:%M:%S")


def s(log_queue, message):
    log_queue.enqueue("{} {} {}".format(Fore.GREEN, _get_time(), message))


def e(log_queue, message):
    log_queue.enqueue("{} {} {}".format(Fore.RED, _get_time(), message))


def i(log_queue, message):
    log_queue.enqueue("{} {} {}".format(Fore.WHITE, _get_time(), message))


def w(log_queue, message):
    log_queue.enqueue("{} {} {}".format(Fore.MAGENTA, _get_time(), message))
