from time import sleep

from api.match_details_api import MatchDetailsApi
from util.api_rate_limit_reached_exception import ApiRateLimitReachedException
from util.log import Log
from worker.worker import Worker


class DetailsWorker(Worker):
    def __init__(self, key, sleep_duration, source, sink):
        self.source = source
        self.sink = sink

        Worker.__init__(self, MatchDetailsApi(), key, sleep_duration)

    def _work(self):
        while True:
            match_id = self.source.dequeue()

            response = None
            while response is None:
                try:
                    response = self.api.request() \
                        .with_key(self.key) \
                        .with_match_id(match_id) \
                        .execute()
                except ApiRateLimitReachedException:
                    Log.e("History worker hit API rate limit, sleeping for {} minutes".format(self.sleep_duration))
                    sleep(self.sleep_duration * 60)

            if "result" not in response or \
                    "match_id" not in response["result"]:
                continue

            Log.s("Requested match with ID {}, received match data with ID {}".format(match_id,
                                                                                      response["result"]["match_id"]))

            self.sink.write(response)
