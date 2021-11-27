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
        return set(Student(*s) for s in self.cursor.fetchall())

    def new_student(self, user_id, name, surname):
        self.cursor.execute(f"INSERT INTO {var.DATABASE_STUDENTS_TABLE} (user_id, name, surname) VALUES (?, ?, ?)", (user_id, name, surname))  # plz, don't do SQL injection on me :(
        self.connection.commit()
        self.students.add(Student(user_id, name, surname))

    def edit_student(self, student, attribute, value):
        self.cursor.execute(f"UPDATE {var.DATABASE_STUDENTS_TABLE} SET {attribute} = ? WHERE user_id = ?", (attribute, value, student.user_id))
        self.connection.commit()
        setattr(student, attribute, value)

    def get_student(self, user_id):
        return next(filter(lambda s: s.user_id == user_id, self.students))
