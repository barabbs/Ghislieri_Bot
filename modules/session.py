from .student import Student
from . import var
import time


class BaseSession(object):
    def __init__(self, user_id):
        self.student = Student(user_id)
        self.message_list = list()
        self.expired = False

    def is_user(self, user_id):
        return self.student.user_id == user_id

    def is_expired(self):
        return self.expired

    def get_last_message(self):
        return self.message_list[-1]

    def handle_response(self, answer_type, value):
        last_message = self.get_last_message()
        answer = getattr(last_message, f'answer_{answer_type}')(value)
        if answer is not None:
            self.update(*answer)

    def update(self, answer):
        pass


class HomeSession(BaseSession):
    pass


class ServiceSession(BaseSession):
    def __init__(self, student):
        super(ServiceSession, self).__init__(student)
        self.last_interaction = None
        self._refresh_last_interaction()

    def _refresh_last_interaction(self):
        self.last_interaction = int(time.time())

    def is_expired(self):
        self.expired = self.expired or (time.time()) > self.last_interaction + var.SERVICE_SESSION_TIMEOUT_SECONDS
        return super(ServiceSession, self).is_expired()

    def handle_response(self, answer_type, value):
        self._refresh_last_interaction()
        super(ServiceSession, self).handle_response(answer_type, value)

    def update(self, *args):
        if args[0] == 'back':
            self.message_list.pop()
        elif args[0] == 'home':
            self.expired = True
        elif args[0] == 'new':
            self.message_list.append(args[1](**args[2]))
