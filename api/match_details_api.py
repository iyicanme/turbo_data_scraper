from api.api import Api
from api.match_details_api_request import MatchDetailsApiRequest


class MatchDetailsApi(Api):
    def __init__(self):
        super().__init__("http://api.steampowered.com/IDOTA2Match_570/GetMatchDetails/v1")

    def request(self):
        return MatchDetailsApiRequest(self.formatted_endpoint)
