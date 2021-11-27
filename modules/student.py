from . import var
import time


class Student(object):
    def __init__(self, user_id, name, surname, email=None):
        self.user_id, self.name, self.surname, self.email = user_id, name, surname, email
        # TODO: Add user permissions
        self.message_list = list()
        self.last_interaction = None
        self.session_expired = False
        self._refresh_last_interaction()

    def _refresh_last_interaction(self):
        self.last_interaction = int(time.time())

    def is_expired(self):
        self.session_expired = self.session_expired or (time.time()) > self.last_interaction + var.SESSION_TIMEOUT_SECONDS
        return self.session_expired

    def get_last_message(self):
        return self.message_list[-1]

    def handle_response(self, answer_type, value):
        self._refresh_last_interaction()
        last_message = self.get_last_message()
        answer = getattr(last_message, f'answer_{answer_type}')(value)
        if answer is not None:
            self.update(*answer)

    def update(self, *args):
        if args[0] == 'back':
            self.message_list.pop()
        elif args[0] == 'home':
            self.expired = True
        elif args[0] == 'new':
            self.message_list.append(args[1](**args[2]))
