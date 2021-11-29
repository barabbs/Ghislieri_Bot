from emoji import emojize
import telegram as tlg
from . import var
from . import formatting as fmt
import logging

log = logging.getLogger(__name__)


def get_back_answer():
    return lambda: ('back',)


def get_home_answer():
    return lambda: ('home',)


def get_new_message_answer(new_msg_class):  # TODO: see if it is better with message instance as argument rather than message class
    return lambda: ('new', new_msg_class, dict())


class BaseMessages(object):
    TITLE = ""
    TEXT = ""

    def __init__(self):
        self.text = self.TEXT

    def _get_text(self):
        return self.TEXT

    def get_content(self):  # TODO: Add Permissions
        content = {'text': emojize(self._get_text()),
                   'parse_mode': tlg.ParseMode.HTML}
        return content

    def get_answer_query(self, query, student):
        pass

    def get_answer_text(self, text, student):
        pass

    # TODO: Add reply for file


class TextMessage(BaseMessages):
    TEXT_ANSWER = lambda: None

    def get_answer_text(self, text, student):
        return self.__class__.TEXT_ANSWER()


class QueryMessage(BaseMessages):
    BUTTONS = list()

    def __init__(self):
        self.buttons = self.BUTTONS.copy()
        self.query_answers = dict()
        super(QueryMessage, self).__init__()

    def _get_buttons(self):
        return self.buttons

    def _set_query_answers(self, buttons):
        self.query_answers = dict()
        for row in buttons:
            for b in row:
                self.query_answers[b[0]] = b[2]

    def get_content(self):
        content = super(QueryMessage, self).get_content()
        buttons = self._get_buttons()
        self._set_query_answers(buttons)
        keyboard = list(list(tlg.InlineKeyboardButton(emojize(b[1]), callback_data=b[0]) for b in row) for row in buttons)
        content['reply_markup'] = tlg.InlineKeyboardMarkup(keyboard)
        return content

    def get_answer_query(self, query, student):
        return self.query_answers[query]()


class NotificationMessage(QueryMessage):
    BUTTONS = [[("ok", "OK", get_home_answer()), ],
               ]


class BackMessage(QueryMessage):

    def _get_buttons(self):
        return super(BackMessage, self)._get_buttons() + [[("back", ":right_arrow_curving_left: Back", get_back_answer()), ], ]
