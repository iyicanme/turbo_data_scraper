import requests


class ApiRequest:
    def __init__(self, endpoint):
        self.endpoint = endpoint
        self.query_parameters = {}

    def with_key(self, key: str):
        self.query_parameters["key"] = key
        return self

    def execute(self):
        return requests.get(self.endpoint, self.query_parameters).json()
