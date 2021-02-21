import requests
import simplejson

from util.exception import ApiRateLimitReachedException, ErroneousResponseException


class ApiRequest:
    def __init__(self, endpoint):
        self.endpoint = endpoint
        self.query_parameters = {}

    def with_key(self, key: str):
        self.query_parameters["key"] = key
        return self

    def execute(self):
        try:
            response = requests.get(self.endpoint, self.query_parameters)
        except requests.exceptions.ConnectionError:
            raise ApiRateLimitReachedException("Hit rate limit when accessing API {} with parameters {}".format(
                self.endpoint,
                self.query_parameters))

        try:
            json_response = response.json()
        except simplejson.errors.JSONDecodeError:
            raise ErroneousResponseException(
                "Received erroneous response with status code {} and content \"{}\"".format(
                    response.status_code,
                    response.text.replace("\n", "")
                ))

        return json_response
