import telegram as tlg
import telegram.ext as tlext
from . import utility as utl
from . import var
from time import sleep
import logging  # TODO: Implement better logging or remove

logger = logging.getLogger(__name__)


class GhislieriBot(tlg.Bot):
    def __init__(self):
        super(GhislieriBot, self).__init__(token=utl.get_bot_token())
        self.updater = tlg.ext.Updater(bot=self)
        self._handlers_setup()
        self.sessions = set()
        self.updater.start_polling()

    def _handlers_setup(self):
        self.updater.dispatcher.add_handler(tlg.ext.CommandHandler('start', self._command_handler))
        self.updater.dispatcher.add_handler(tlg.ext.CallbackQueryHandler(lambda u, c: self._callback_handler))
        self.updater.dispatcher.add_handler(tlg.ext.MessageHandler(tlg.ext.Filters.text & (~tlg.ext.Filters.command), self._message_handler))
        self.updater.dispatcher.add_error_handler(self._error_handler)
        # TODO: Add Files Handler

    def _get_session(self, update):
        try:
            return next(filter(lambda s: s.is_user(update.effective_user.id), self.sessions))
        except StopIteration:
            raise  # TODO: Add new user sign-up

    def _command_handler(self, update, context):
        pass

    def _error_handler(self, update, context):
        logger.error(msg="Exception while handling an update:", exc_info=context.error)
        print(context.error)  # TODO: Implement error logging and sending to admins

    def _callback_handler(self, update, context):
        self._response_handler(self._get_session(update), 'callback', update.callback_query.data, True)

    def _message_handler(self, update, context):
        self._response_handler(self._get_session(update), 'message', update.update.message.text)

    def _response_handler(self, session, answer_type, value, edit=False):
        to_update = session.handle_response(answer_type, value)
        if to_update:
            self._chat_update(session, edit)

    def _chat_update(self, session, edit):
        pass

    def run(self):
        try:
            while True:
                sleep(1)  # TODO: Add expired session control and reset
        except KeyboardInterrupt:
            pass
        finally:
            self.quit()

    def quit(self):
        pass  # TODO: Terminating procedures
