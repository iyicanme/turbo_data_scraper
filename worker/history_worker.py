from api.game_modes import GameMode
from api.match_history_api import MatchHistoryApi
from util.log import Log
from worker.worker import Worker


class HistoryWorker(Worker):
    def __init__(self, key, sink, start_match_id, matches_requested=100):
        self.start_match_id = start_match_id
        self.matches_requested = matches_requested
        self.sink = sink

        Worker.__init__(self, MatchHistoryApi(), key)

    def _work(self):
        last_match_id = self.start_match_id

        Log.i("History worker started")

        while True:
            response = self.api.request() \
                .with_key(self.key) \
                .with_game_mode(GameMode.TURBO) \
                .with_start_at_match_id(self.start_match_id) \
                .with_matches_requested(self.matches_requested) \
                .execute()

            Log.i("Received history response")

            if response is None or \
                    "result" not in response or \
                    "num_results" not in response["result"] or \
                    response["result"]["num_results"] == 0:
                continue

            Log.s("Worker thread received {} match IDs".format(response["result"]["num_results"]))

            for match in response["result"]["matches"]:
                self.sink.enqueue(int(match["match_id"]))

            next_match_id = int(response["result"]["matches"][-1]["match_id"]) + 1
            Log.s("Updated last match ID {} with {}".format(last_match_id, next_match_id))
            last_match_id = next_match_id
