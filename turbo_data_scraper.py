from log.logger import Logger
from queueing.broker import Broker
from queueing.dealer import Dealer
from sink.file_sink import FileSink
from util.config import Config
from worker.details_worker import DetailsWorker
from worker.history_worker import HistoryWorker


def run_turbo_data_scraper():
    worker_list = []
    log_broker = Broker()
    logger = Logger(log_broker)
    worker_list.append(logger)

    config = Config()

    id_dealer = Dealer()

    worker = HistoryWorker(config.get_api_key(),
                           config.get_sleep_duration(),
                           log_broker.create_queue(),
                           sink=id_dealer,
                           start_match_id=config.get_start_match_id(),
                           matches_requested=config.get_matches_requested())
    worker_list.append(worker)

    for i in range(config.get_worker_count()):
        worker = DetailsWorker(config.get_api_key(),
                               config.get_sleep_duration(),
                               log_broker.create_queue(),
                               source=id_dealer.create_queue(),
                               sink=FileSink(path=config.get_data_path(),
                                             file_name_pattern=config.get_file_name_pattern(),
                                             unique_id=config.get_worker_name_pattern().format(i + 1),
                                             max_size=pow(2, config.get_file_size_binary_power())))
        worker_list.append(worker)

    for worker in worker_list:
        worker.start()

    for worker in worker_list:
        worker.join()


if __name__ == '__main__':
    run_turbo_data_scraper()
