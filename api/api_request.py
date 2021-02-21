import requests

from util.api_rate_limit_reached_exception import ApiRateLimitReachedException
from util.log import Log


class ApiRequest:
    def __init__(self, endpoint):
        self.endpoint = endpoint
        self.query_parameters = {}

    def with_key(self, key: str):
        self.query_parameters["key"] = key
        return self

    def execute(self):
        try:
            return requests.get(self.endpoint, self.query_parameters).json()
        except requests.exceptions.ConnectionError:
            Log.e("Hit rate limit when accessing API {} with paramters {}".format(self.endpoint, self.query_parameters))
            raise ApiRateLimitReachedException
