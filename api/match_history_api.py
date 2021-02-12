from api.api import Api
from api.match_history_api_request import MatchHistoryApiRequest


class MatchHistoryApi(Api):
    def __init__(self):
        super().__init__("http://api.steampowered.com/IDOTA2Match_570/GetMatchHistory/v1")

    def request(self):
        return MatchHistoryApiRequest(self.formatted_endpoint)
