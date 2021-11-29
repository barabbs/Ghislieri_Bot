import telegram as tlg
import telegram.ext
from messages.welcome import WelcomeMessage
from .databaser import Databaser
from . import telegram_errors as tlgerr
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
        self.databaser = Databaser()
        self.updater.start_polling()

    def _handlers_setup(self):
        self.updater.dispatcher.add_handler(tlg.ext.CommandHandler('start', self._command_handler))
        self.updater.dispatcher.add_handler(tlg.ext.CallbackQueryHandler(self._query_handler))
        self.updater.dispatcher.add_handler(tlg.ext.MessageHandler(tlg.ext.Filters.text & (~tlg.ext.Filters.command), self._text_handler))
        self.updater.dispatcher.add_error_handler(self._error_handler)
        # TODO: Add Files Handler

    def _get_student(self, update):
        student = self.databaser.get_student(update.effective_user.id)
        if student is not None:
            return student
        else:
            return self._new_student_signup(update)

    def _new_student_signup(self, update):
        welcome_msg = WelcomeMessage()
        new_msg_id = self.send_message(chat_id=update.message.chat.id, **welcome_msg.get_content())  # TODO: Visual bug - message gets sent and then deleted inside _command_handler
        student = self.databaser.new_student(update.effective_user.id, update.message.chat.id, new_msg_id.message_id)
        student.add_reset_message(welcome_msg)
        return student

    def _error_handler(self, update, context):
        logger.error(msg="Exception while handling an update:", exc_info=context.error)
        print(context.error)  # TODO: Implement error logging and sending to admins

    def _command_handler(self, update, context):
        student = self._get_student(update)
        student.reset_session()
        self._send_message(student)

    def _query_handler(self, update, context):
        student = self._get_student(update)
        student.respond('query', update.callback_query.data)
        self._send_message(student, True)

    def _text_handler(self, update, context):
        student = self._get_student(update)
        student.respond('text', update.message.text)
        self._send_message(student)

    def _send_message(self, student, edit=False):
        message_content = student.get_message_content()
        if edit:
            self._edit_message(student, message_content)
        else:
            self._send_and_delete_message(student, message_content)

    def _edit_message(self, student, message_content):
        try:
            self.edit_message_text(**message_content)
        except telegram.error.BadRequest as e:
            if e.message == tlgerr.EDIT_MSG_NOT_FOUND:
                self._send_and_delete_message(student, message_content)
            elif e.message != tlgerr.EDIT_MSG_IDENTICAL:
                raise  # TODO: Do this better

    def _send_and_delete_message(self, student, message_content):
        try:
            self.delete_message(chat_id=message_content['chat_id'], message_id=message_content['message_id'])
        except telegram.error.BadRequest as e:
            if e.message != tlgerr.DELETE_MSG_NOT_FOUND:
                raise  # TODO: Do this better
        message_content.pop('message_id')
        new_message = self.send_message(**message_content)
        self.databaser.set_student_last_message_id(student, new_message.message_id)

    def run(self):
        try:
            while True:
                for s in self.databaser.get_students():
                    update_edit = s.update()
                    if update_edit is not None:
                        self._send_message(s, update_edit)
                sleep(var.STUDENT_UPDATE_SECONDS_INTERVAL)
        except KeyboardInterrupt:
            print("Keyboard Interrupt - Exiting...")
        self.quit()

    def quit(self):
        self.updater.dispatcher.stop()
        self.databaser.exit()
        pass  # TODO: Terminating procedures
        print("Ghislieri Bot ended")
