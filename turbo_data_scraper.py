from queuing.broker import Broker
from queuing.dealer import Dealer

from log.logger import Logger
from sink.file_sink import FileSink
from util.config import Config
from worker.details_worker import DetailsWorker
from worker.history_worker import HistoryWorker


class TurboDataScraper:
    def __init__(self):
        if not TurboDataScraper.config_exists():
            TurboDataScraper.create_empty_config_file()
            exit(1)

        self.log_broker = Broker()
        self.logger = Logger(self.log_broker)

        self.config = Config()

        self.id_dealer = Dealer()
        self.history_worker = HistoryWorker(self.config.get_history_worker_api_key(),
                                            self.config.get_sleep_duration(),
                                            self.log_broker.create_queue(),
                                            sink=self.id_dealer,
                                            start_match_id=self.config.get_start_match_id(),
                                            matches_requested=self.config.get_matches_requested())

        self.workers = []
        for i, api_key in enumerate(self.config.get_details_workers_api_keys()):
            worker = DetailsWorker(api_key,
                                   self.config.get_sleep_duration(),
                                   self.log_broker.create_queue(),
                                   source=self.id_dealer.create_queue(),
                                   sink=FileSink(path=self.config.get_data_path(),
                                                 file_name_pattern=self.config.get_file_name_pattern(),
                                                 unique_id=self.config.get_worker_name_pattern().format(i + 1),
                                                 max_size=pow(2, self.config.get_file_size_binary_power())))
            self.workers.append(worker)

    def start(self):
        self.logger.start()

        self.history_worker.start()

        for worker in self.workers:
            worker.start()

        return self

    def join(self):
        for worker in self.workers:
            worker.join()

        self.history_worker.join()

        self.logger.join()

    @staticmethod
    def config_exists():
        from os.path import exists

        return exists("config.json")

    @staticmethod
    def create_empty_config_file():
        if TurboDataScraper.config_exists():
            return

        config = {
            "history_worker_api_key": "",
            "details_workers_api_keys": [],
            "start_match_id": 0,
            "matches_requested": 0,
            "data_path": "",
            "file_name_pattern": "",
            "worker_name_pattern": "",
            "file_size_binary_power": 0,
            "sleep_duration": 0
        }

        from json import dump
        with open("config.json", "w") as config_file:
            dump(config, config_file)


if __name__ == '__main__':
    TurboDataScraper().start().join()
