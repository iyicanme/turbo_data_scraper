from sink.file_sink import FileSink
from util.config import Config
from util.id_queue import IdQueue
from util.log import Log
from worker.details_worker import DetailsWorker
from worker.history_worker import HistoryWorker


def run_turbo_data_scraper():
    Log()
    config = Config()

    queue = IdQueue()

    HistoryWorker(config.get_api_key(),
                  queue,
                  config.get_start_match_id(),
                  config.get_matches_requested()).start()

    for i in range(1, config.get_worker_count() + 1):
        DetailsWorker(config.get_api_key(),
                      queue,
                      FileSink(config.get_data_path(),
                               config.get_file_name_pattern(),
                               config.get_worker_name_pattern().format(i),
                               pow(2, config.get_file_size_binary_power()))).start()


if __name__ == '__main__':
    run_turbo_data_scraper()
