from modules import basemessages as bmsg
import importlib


class HomeMessage(bmsg.QueryMessage):
    TEXT = f":red_circle::yellow_circle: Collegio Ghislieri :red_circle::yellow_circle:"
    BOT_SERVICES = ('ghislieri_bot',)

    def __init__(self):
        super(HomeMessage, self).__init__()
        self.service_modules = dict()
        for service in self.BOT_SERVICES:
            service_module = importlib.import_module(f"messages.{service}.main")
            self.service_modules[service] = service_module
            setattr(self, f'_query_{service}', bmsg.get_new_message_answer(service_module.MainMessage))

    def _get_buttons(self):
        return list([(self.service_modules[service].SERVICE_NAME, service), ] for service in self.BOT_SERVICES)
