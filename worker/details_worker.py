from api.match_details_api import MatchDetailsApi
from util.log import Log
from worker.worker import Worker


class DetailsWorker(Worker):
    def __init__(self, key, source, sink):
        self.source = source
        self.sink = sink
        Worker.__init__(self, MatchDetailsApi(), key)

    def _work(self):
        while True:
            match_id = self.source.dequeue()

            response = self.api.request() \
                .with_key(self.key) \
                .with_match_id(match_id) \
                .execute()

            if response is None or \
                    "result" not in response or \
                    "match_id" not in response["result"]:
                continue

            Log.s("Requested match with ID {}, received match data with ID {}".format(match_id,
                                                                                      response["result"]["match_id"]))

            self.sink.write(response)
