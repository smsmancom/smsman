class Error(Exception):
    pass


class ClientError(Error):
    def __init__(self, error_message):
        self.error_message = error_message
