from . import var
import time
from messages.home import HomeMessage


class Student(object):
    def __init__(self, user_id, chat_id, last_message_id, infos=None):
        self.user_id, self.chat_id, self.last_message_id = user_id, chat_id, last_message_id
        if infos is None:
            infos = dict((k, None) for k in var.STUDENT_INFOS)
        self.infos = infos
        self.message_list = list()
        self.last_interaction = None
        self._refresh_last_interaction()
        # TODO: Add user permissions

    def _set_first_message(self):
        self.message_list = [HomeMessage(), ]  # TODO: Add notification support
        return False  # TODO: return True if message is notification

    def _get_message(self):
        return self.message_list[-1]

    def respond(self, response_type, value):
        self._refresh_last_interaction()
        answer = self._get_answer(response_type, value)
        if answer is not None:
            self._response_update(*answer)

    def _refresh_last_interaction(self):
        self.last_interaction = int(time.time())

    def _get_answer(self, response_type, value):
        last_message = self._get_message()
        return getattr(last_message, f'get_answer_{response_type}')(value)

    def _response_update(self, *args):
        if args[0] == 'back':
            self.message_list.pop()
        elif args[0] == 'home':
            self._set_first_message()
        elif args[0] == 'new':
            self.message_list.append(args[1](**args[2]))

    def get_message_content(self):
        message = self._get_message()
        content = message.get_content()
        content.update({'chat_id': self.chat_id, 'message_id': self.last_message_id})

    def update(self):
        if self._is_session_expired():
            return self._set_first_message()

    def _is_session_expired(self):
        return (time.time()) > self.last_interaction + var.SESSION_TIMEOUT_SECONDS and len(self.message_list) > 1
