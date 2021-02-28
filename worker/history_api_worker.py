from time import sleep

from api.game_modes import GameMode
from api.match_history_api import MatchHistoryApi
from util import log
from util.exception import ApiRateLimitReachedException, ErroneousResponseException
from util.synchronized_printer import SynchronizedPrinter
from worker.api_worker import ApiWorker


class HistoryApiWorker(ApiWorker):
    def __init__(self, key, sleep_duration, log_queue, sink, dump_path, start_match_id, matches_requested=100):
        ApiWorker.__init__(self, MatchHistoryApi(), key, sleep_duration, log_queue)

        self.dump_path = dump_path
        self.start_match_id = start_match_id
        self.matches_requested = matches_requested
        self.sink = sink

        self.last_match_id = start_match_id

    def _work(self):
        response = None
        while response is None:
            try:
                response = self.api.request() \
                    .with_key(self.key) \
                    .with_game_mode(GameMode.TURBO) \
                    .with_start_at_match_id(self.start_match_id) \
                    .with_matches_requested(self.matches_requested) \
                    .execute()
            except ApiRateLimitReachedException as ex:
                log.e(self.log_queue, "History worker exception: {}, sleeping for {} minutes".format(
                    ex.message,
                    self.sleep_duration))
                sleep(self.sleep_duration * 60)
            except ErroneousResponseException as ex:
                log.e(self.log_queue, "Details worker exception: {}, sleeping for {} minutes".format(
                    ex.message,
                    self.sleep_duration))
                sleep(self.sleep_duration * 60)

        log.i(self.log_queue, "Received history response")

        if "result" not in response or \
                "num_results" not in response["result"] or \
                response["result"]["num_results"] == 0:
            return

        log.s(self.log_queue, "Worker thread received {} match IDs".format(response["result"]["num_results"]))

        for match in response["result"]["matches"]:
            self.sink.enqueue(int(match["match_id"]))

        next_match_id = int(response["result"]["matches"][-1]["match_id"]) + 1
        log.s(self.log_queue, "Updated last match ID {} with {}".format(self.last_match_id, next_match_id))
        self.last_match_id = next_match_id

    def _cleanup(self):
        pending_match_ids = self.sink.get_contents()

        from json import dump
        with open("{}/history.json".format(self.dump_path), "w") as dump_file:
            dump(pending_match_ids, dump_file)

        SynchronizedPrinter().print_synchronized("History worker cleaned up")
