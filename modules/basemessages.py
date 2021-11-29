from emoji import emojize
import telegram as tlg
from . import var
from . import formatting as fmt


def _get_back_answer():
    return lambda: ('back',)


def _get_home_answer():
    return lambda: ('home',)


def _get_new_message_answer(new_msg_class):
    return lambda: ('new', new_msg_class)


class BaseMessages(object):
    TEXT = ""

    def __init__(self):
        self.text = self.TEXT

    def _get_text(self):
        return self.TEXT

    def get_content(self):  # TODO: Add Permissions
        content = {'text': emojize(fmt.sanify(self._get_text())),
                   'parse_mode': tlg.ParseMode.HTML}
        return content

    def get_answer_query(self, query):
        pass

    def get_answer_message(self, text):
        pass

    # TODO: Add reply for file


class QueryMessage(BaseMessages):
    BUTTONS = list()

    def __init__(self):
        self.buttons = self.BUTTONS.copy()
        super(QueryMessage, self).__init__()

    def _get_buttons(self):
        return self.buttons

    def get_content(self):
        content = super(QueryMessage, self).get_content()
        keyboard = list(list(tlg.InlineKeyboardButton(emojize(fmt.sanify(b[0])), callback_data=b[1]) for b in row) for row in self._get_buttons())
        content['reply_markup'] = tlg.InlineKeyboardMarkup(keyboard)
        return content

    def get_answer_query(self, query):
        return getattr(self, f'_query_{query}')()


class NotificationMessage(QueryMessage):
    BUTTONS = [[("OK", "ok"), ],
               ]

    def __init__(self):
        self._query_ok = _get_home_answer()
        super(NotificationMessage, self).__init__()
