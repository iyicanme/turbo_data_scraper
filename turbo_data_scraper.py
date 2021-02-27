from queuing.broker import Broker
from queuing.dealer import Dealer
from sink.file_sink import FileSink
from util.config import Config
from util.log import init_logging
from worker.details_api_worker import DetailsApiWorker
from worker.history_api_worker import HistoryApiWorker
from worker.log_worker import LogWorker


class TurboDataScraper:
    def __init__(self):
        init_logging()

        if not Config.exists():
            Config.create_blank()
            exit(1)

        self.config = Config()

        self.log_broker = Broker()
        self.log_worker = LogWorker(self.log_broker, self.config.get_dump_path())

        self.id_dealer = Dealer()
        self.history_worker = HistoryApiWorker(self.config.get_history_worker_api_key(),
                                               self.config.get_sleep_duration(),
                                               self.log_broker.create_queue(),
                                               sink=self.id_dealer,
                                               dump_path=self.config.get_dump_path(),
                                               start_match_id=self.config.get_start_match_id(),
                                               matches_requested=self.config.get_matches_requested())

        self.workers = []
        for i, api_key in enumerate(self.config.get_details_workers_api_keys()):
            worker = DetailsApiWorker(api_key,
                                      self.config.get_sleep_duration(),
                                      self.log_broker.create_queue(),
                                      source=self.id_dealer.create_queue(),
                                      sink=FileSink(path=self.config.get_data_path(),
                                                    file_name_pattern=self.config.get_file_name_pattern(),
                                                    unique_id=self.config.get_worker_name_pattern().format(i + 1),
                                                    max_size=pow(2, self.config.get_file_size_binary_power())))
            self.workers.append(worker)

    def start(self):
        self.log_worker.start()

        self.history_worker.start()

        for worker in self.workers:
            worker.start()

        return self

    def join(self):
        for worker in self.workers:
            worker.join()

        self.history_worker.join()

        self.log_worker.join()


if __name__ == '__main__':
    TurboDataScraper().start().join()
