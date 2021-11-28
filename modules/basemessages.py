from emoji import emojize
import telegram as tlg
from . import var
from . import formatting as fmt


class BaseMessages(object):
    TEXT = ""

    def _get_text(self):
        return self.TEXT

    def get_content(self):  # TODO: Add Permissions
        message = {'text': emojize(fmt.sanify(self._get_text())),
                   'parse_mode': tlg.ParseMode.HTML}
        return message

    def get_answer_query(self, callback):
        pass

    def get_answer_message(self, text):
        pass

    # TODO: Add reply for file


class QueryMessage(BaseMessages):
    pass
