from modules import basemessages as bmsg
import importlib


class HomeMessage(bmsg.QueryMessage):
    TEXT = f":red_circle::yellow_circle: {bmsg.fmt.bold('Home')} :red_circle::yellow_circle:"
    BOT_SERVICES = ('ghislieri_bot',)

    def _get_buttons(self, **kwargs):
        buttons = list()
        for service in self.BOT_SERVICES:
            message = importlib.import_module(f"messages.{service}.main").MainMessage
            buttons.append([(service, message.TITLE, bmsg.get_new_message_answer(message)), ])
        return buttons
