import os, datetime, traceback
from . import var

EDIT_MSG_NOT_FOUND = "Message to edit not found"
EDIT_MSG_IDENTICAL = "Message is not modified: specified new message content and reply markup are exactly the same as a current content and reply markup of the message"
DELETE_MSG_NOT_FOUND = "Message to delete not found"


def log_error(error, student=None):
    time = datetime.datetime.now().strftime(var.DATETIME_FORMAT)
    header = (f"name={student.get_info('name')}\nsurname={student.get_info('surname')}\n" if student is not None else "") + f"user_id={student.user_id}\ntime={time}"
    error_str = ''.join(traceback.format_exception(None, error, error.__traceback__))
    with open(os.path.join(var.ERRORS_DIR, f"{time}.gber"), 'w', encoding='utf-8') as f:
        f.write(f"{header}\n\n{error_str}")
