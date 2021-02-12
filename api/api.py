from abc import ABC, abstractmethod


class Api(ABC):
    def __init__(self, endpoint, path_parameters=None):
        self.endpoint = endpoint
        self.path_parameters = path_parameters

        self.formatted_endpoint = endpoint.format(path_parameters)

    @abstractmethod
    def request(self):
        pass
