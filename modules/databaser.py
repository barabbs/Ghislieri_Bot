import sqlite3 as sql
from .student import Student
import threading as thr
import queue
from . import var


class Databaser(object):
    def __init__(self):
        self.requests_queue, self.results_queue = queue.Queue(), queue.Queue()
        self.process = DatabaserThread(self.requests_queue, self.results_queue)
        self.process.start()

    def _put_request_get_result(self, method, *args):  # TODO: Maybe rewrite with decorator?
        self.requests_queue.put((method, args), block=True)
        return self.results_queue.get(block=True)

    def new_student(self, user_id, chat_id, last_message_id):
        return self._put_request_get_result('new_student', user_id, chat_id, last_message_id)

    def edit_student_info(self, student, info, value):
        return self._put_request_get_result('edit_student_info', student, info, value)

    def set_student_chat_id(self, student, chat_id):
        return self._put_request_get_result('set_student_chat_id', student, chat_id)

    def set_student_last_message_id(self, student, last_message_id):
        return self._put_request_get_result('set_student_last_message_id', student, last_message_id)

    def get_student(self, user_id):
        return self._put_request_get_result('get_student', user_id)

    def get_students(self):
        return self._put_request_get_result('get_students')

    def exit(self):
        return self._put_request_get_result('exit')


class DatabaserThread(thr.Thread):
    def __init__(self, requests_queue, results_queue):
        self.requests_queue, self.results_queue = requests_queue, results_queue
        self.connection, self.cursor, self.students = None, None, None
        super(DatabaserThread, self).__init__()

    def _load_database(self):
        self.connection = sql.connect(var.FILEPATH_DATABASE)
        self.cursor = self.connection.cursor()

    def _load_students(self):
        self.cursor.execute(f"SELECT * FROM {var.DATABASE_STUDENTS_TABLE}")
        self.students = set(Student(*s[0:3], infos=dict(zip(var.STUDENT_INFOS, s[3:]))) for s in self.cursor.fetchall())

    def _new_student(self, user_id, chat_id, last_message_id):
        self.cursor.execute(f"INSERT INTO {var.DATABASE_STUDENTS_TABLE} (user_id, chat_id, last_message_id) VALUES (?, ?, ?)",
                            (user_id, chat_id, last_message_id))  # plz, don't do SQL injection on me :(
        self.connection.commit()
        new_student = Student(user_id, chat_id, last_message_id)
        self.students.add(new_student)
        return new_student

    def _edit_database(self, student, attribute, value):
        self.cursor.execute(f"UPDATE {var.DATABASE_STUDENTS_TABLE} SET {attribute} = ? WHERE user_id = ?", (value, student.user_id))
        self.connection.commit()

    def _edit_student_info(self, student, info, value):
        self._edit_database(student, info, value)
        student.infos[info] = value

    def _set_student_chat_id(self, student, chat_id):
        self._edit_database(student, 'chat_id', chat_id)
        student.chat_id = chat_id

    def _set_student_last_message_id(self, student, last_message_id):
        self._edit_database(student, 'last_message_id', last_message_id)
        student.last_message_id = last_message_id

    def _get_student(self, user_id):
        try:
            return next(filter(lambda s: s.user_id == user_id, self.students))
        except StopIteration:
            return None

    def _get_students(self):
        return self.students

    def _exit(self):
        self.connection.commit()
        self.cursor.close()
        self.connection.close()

    def run(self):
        self._load_database()
        self._load_students()
        while True:
            method, args = self.requests_queue.get(block=True)
            result = getattr(self, f'_{method}')(*args)
            self.results_queue.put(result, block=True)
            if method == 'exit':
                break
        print("Databaser Thread ended")
