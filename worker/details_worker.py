from time import sleep

from api.match_details_api import MatchDetailsApi
from log.logger import Logger
from util.exception import ApiRateLimitReachedException, ErroneousResponseException
from worker.worker import Worker


class DetailsWorker(Worker):
    def __init__(self, key, sleep_duration, log_queue, source, sink):
        Worker.__init__(self, MatchDetailsApi(), key, sleep_duration, log_queue)

        self.source = source
        self.sink = sink

    def _work(self):
        while True:
            match_id = self.source.dequeue()

            if match_id is None:
                continue

            response = None
            while response is None:
                try:
                    response = self.api.request() \
                        .with_key(self.key) \
                        .with_match_id(match_id) \
                        .execute()
                except ApiRateLimitReachedException as ex:
                    Logger.e(self.log_queue, "Details worker exception: {}, sleeping for {} minutes".format(
                        ex.message,
                        self.sleep_duration))
                    sleep(self.sleep_duration * 60)
                except ErroneousResponseException as ex:
                    Logger.e(self.log_queue, "Details worker exception: {}, sleeping for {} minutes".format(
                        ex.message,
                        self.sleep_duration))
                    sleep(self.sleep_duration * 60)

            if "result" not in response or "match_id" not in response["result"]:
                continue

            Logger.s(self.log_queue, "Requested match with ID {}, received match data with ID {}".format(
                match_id,
                response["result"]["match_id"]))

            self.sink.write(response)
