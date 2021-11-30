import os, datetime, traceback
from . import var


def log_error(error, student=None, severity="error"):
    time = datetime.datetime.now().strftime(var.DATETIME_FORMAT)
    header = f"severity={severity}\n" + (f"name={student.get_info('name')}\nsurname={student.get_info('surname')}\nuser_id={student.user_id}\n" if student is not None else "") + f"time={time}"
    error_str = ''.join(traceback.format_exception(None, error, error.__traceback__))
    with open(os.path.join(var.ERRORS_DIR, f"{severity}_{time}.gber"), 'w', encoding='utf-8') as f:
        f.write(f"{header}\n--------------------------------\n{error_str}")
