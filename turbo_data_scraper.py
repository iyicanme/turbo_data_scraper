from sink.file_sink import FileSink
from util.config import Config
from util.id_dealer import IdDealer
from util.log import Log
from worker.details_worker import DetailsWorker
from worker.history_worker import HistoryWorker


def run_turbo_data_scraper():
    Log()
    config = Config()
    worker_list = []

    dealer = IdDealer(config.get_worker_count())

    worker = HistoryWorker(config.get_api_key(),
                           config.get_sleep_duration(),
                           sink=dealer,
                           start_match_id=config.get_start_match_id(),
                           matches_requested=config.get_matches_requested()).start()
    worker_list.append(worker)

    for i in range(config.get_worker_count()):
        worker = DetailsWorker(config.get_api_key(),
                               config.get_sleep_duration(),
                               source=dealer.get_queue(i),
                               sink=FileSink(path=config.get_data_path(),
                                             file_name_pattern=config.get_file_name_pattern(),
                                             unique_id=config.get_worker_name_pattern().format(i + 1),
                                             max_size=pow(2, config.get_file_size_binary_power()))).start()
        worker_list.append(worker)

    for worker in worker_list:
        worker.join()


if __name__ == '__main__':
    run_turbo_data_scraper()
