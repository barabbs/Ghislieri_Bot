import sqlite3 as sql
from .student import Student
from . import var


class Databaser(object):
    def __init__(self):
        self.connection = sql.connect(var.FILEPATH_DATABASE)
        self.cursor = self.connection.cursor()
        self.students = self._load_students()

    def _load_students(self):
        self.cursor.execute(f"SELECT * FROM {var.DATABASE_STUDENTS_TABLE}")
        return set(Student(*s[0:2], infos=dict(zip(var.STUDENT_INFOS, s[2:]))) for s in self.cursor.fetchall())

    def new_student(self, user_id, chat_id, last_message_id, start_message):
        self.cursor.execute(f"INSERT INTO {var.DATABASE_STUDENTS_TABLE} (user_id, chat_id, last_message_id) VALUES (?, ?, ?)",
                            (user_id, chat_id, last_message_id))  # plz, don't do SQL injection on me :(
        self.connection.commit()
        new_student = Student(user_id, chat_id, last_message_id, start_message=start_message)
        self.students.add(new_student)
        return new_student

    def _edit_database(self, student, attribute, value):
        self.cursor.execute(f"UPDATE {var.DATABASE_STUDENTS_TABLE} SET {attribute} = ? WHERE user_id = ?", (attribute, value, student.user_id))
        self.connection.commit()

    def edit_student_info(self, student, info, value):
        self._edit_database(student, info, value)
        student.infos[info] = value

    def set_student_chat_id(self, student, chat_id):
        self._edit_database(student, 'chat_id', chat_id)
        student.chat_id = chat_id

    def set_student_last_message_id(self, student, last_message_id):
        self._edit_database(student, 'last_message_id', last_message_id)
        student.last_message_id = last_message_id

    def get_student(self, user_id):
        return next(filter(lambda s: s.user_id == user_id, self.students))

    def get_students(self):
        return self.students
