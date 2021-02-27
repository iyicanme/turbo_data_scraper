from time import sleep

from api.match_details_api import MatchDetailsApi
from util import log
from util.exception import ApiRateLimitReachedException, ErroneousResponseException
from worker.api_worker import ApiWorker


class DetailsApiWorker(ApiWorker):
    def __init__(self, key, sleep_duration, log_queue, source, sink):
        ApiWorker.__init__(self, MatchDetailsApi(), key, sleep_duration, log_queue)

        self.source = source
        self.sink = sink

    def _work(self):
        match_id = self.source.dequeue()

        if match_id is None:
            return

        response = None
        while response is None:
            try:
                response = self.api.request() \
                    .with_key(self.key) \
                    .with_match_id(match_id) \
                    .execute()
            except ApiRateLimitReachedException as ex:
                log.e(self.log_queue, "Details worker exception: {}, sleeping for {} minutes".format(
                    ex.message,
                    self.sleep_duration))
                sleep(self.sleep_duration * 60)
            except ErroneousResponseException as ex:
                log.e(self.log_queue, "Details worker exception: {}, sleeping for {} minutes".format(
                    ex.message,
                    self.sleep_duration))
                sleep(self.sleep_duration * 60)

        if "result" not in response or "match_id" not in response["result"]:
            return

        log.s(self.log_queue, "Requested match with ID {}, received match data with ID {}".format(
            match_id,
            response["result"]["match_id"]))

        self.sink.write(response)

    def _cleanup(self):
        self.sink.close()
