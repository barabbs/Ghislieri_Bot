from . import var


class BaseMessages(object):
    def __init__(self, last_message):
        self.last_mesage = last_message

    def send(self):
        pass

    def answer_callback(self, callback):
        pass

    def answer_message(self, text):
        pass

    # TODO: Add reply for file

class CallBackMessage(BaseMessages):
    pass
