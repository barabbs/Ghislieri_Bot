import telegram as tlg
import telegram.ext
from messages.welcome import WelcomeMessage
from .databaser import Databaser
from . import telegram_errors as tlgerr
from . import utility as utl
from . import var
from time import sleep
import logging

log = logging.getLogger(__name__)


def get_bot_token():
    with open(var.FILEPATH_BOT_TOKEN, 'r') as token_file:
        return token_file.readline()


class GhislieriBot(tlg.Bot):
    def __init__(self):
        log.info("Bot creating...")
        super(GhislieriBot, self).__init__(token=get_bot_token())
        self.updater = tlg.ext.Updater(bot=self)
        self._handlers_setup()
        self.databaser = Databaser()
        self.updater.start_polling()
        log.info("Bot created")

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
        log.info(f"Found new student with user_id {update.effective_user.id}")
        welcome_msg = WelcomeMessage()
        new_msg_id = self.send_message(chat_id=update.message.chat.id, **welcome_msg.get_content())  # TODO: Visual bug - message gets sent and then deleted inside _command_handler
        student = self.databaser.new_student(update.effective_user.id, update.message.chat.id, new_msg_id.message_id)
        student.add_reset_message(welcome_msg)
        return student

    def _error_handler(self, update, context):
        log.error(f"Exception while handling an update: {context.error}")
        try:
            student = self.databaser.get_student(update.effective_user.id)
        except Exception:  # TODO: See if there's a better way to do this
            student = None
        utl.log_error(context.error, student)

    def _command_handler(self, update, context):
        student = self._get_student(update)
        student.reset_session()
        self._send_message(student, del_user_msg=update.message.message_id)

    def _query_handler(self, update, context):
        student = self._get_student(update)
        student.respond('query', update.callback_query.data, databaser=self.databaser)
        self._send_message(student, edit=True)

    def _text_handler(self, update, context):
        student = self._get_student(update)
        student.respond('text', update.message.text, databaser=self.databaser)
        self._send_message(student, del_user_msg=update.message.message_id)

    def _send_message(self, student, edit=False, del_user_msg=None):
        message_content = student.get_message_content()
        if edit:
            self._edit_message(student, message_content)
        else:
            self._send_and_delete_message(student, message_content, del_user_msg)

    def _edit_message(self, student, message_content):
        try:
            self.edit_message_text(**message_content)
        except telegram.error.BadRequest as e:
            if e.message == tlgerr.EDIT_MSG_NOT_FOUND:
                log.warning(e.message)
                self._send_and_delete_message(student, message_content)
            elif e.message == tlgerr.EDIT_MSG_IDENTICAL:
                log.warning(e.message)
            else:
                log.error(f"Exception while editing a message: {e}")
                utl.log_error(e)

    def _send_and_delete_message(self, student, message_content, del_user_msg=None):
        try:
            self.delete_message(chat_id=message_content['chat_id'], message_id=message_content['message_id'])
            if del_user_msg is not None:
                self.delete_message(chat_id=message_content['chat_id'], message_id=del_user_msg)
        except telegram.error.BadRequest as e:
            if e.message == tlgerr.DELETE_MSG_NOT_FOUND:
                log.warning(e.message)
            else:
                log.error(f"Exception while sending and deleting a message: {e}")
                utl.log_error(e)
        message_content.pop('message_id')
        new_message = self.send_message(**message_content)
        self.databaser.set_student_last_message_id(student, new_message.message_id)

    def run(self):
        log.info("Bot started")
        try:
            while True:
                for s in self.databaser.get_students():
                    update_edit = s.update()
                    if update_edit is not None:
                        self._send_message(s, edit=update_edit)
                sleep(var.STUDENT_UPDATE_SECONDS_INTERVAL)
        except KeyboardInterrupt:
            log.info("Bot received exit signal")
        finally:
            self.exit()
        log.info("Bot finished")

    def exit(self):
        log.info("Bot exiting...")
        self.updater.dispatcher.stop()
        self.databaser.exit()
        pass  # TODO: Terminating procedures
        log.info("Bot exited")
