from api.api_request import ApiRequest


class MatchDetailsApiRequest(ApiRequest):
    def __init__(self, endpoint):
        super().__init__(endpoint)

    def with_match_id(self, match_id: int):
        self.query_parameters["match_id"] = str(match_id)
        return self
