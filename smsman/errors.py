class Error(Exception):
    pass


class WrongTokenError(Error):
    def __init__(self, error_message):
        self.error_message = error_message


class SMSnotReceivedError(Error):
    def __init__(self, error_message):
        self.error_message = error_message


