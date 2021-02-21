class ApiRateLimitReachedException(Exception):
    def __init__(self, message):
        self.message = message


class ErroneousResponseException(Exception):
    def __init__(self, message):
        self.message = message
