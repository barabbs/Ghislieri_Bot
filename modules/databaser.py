import sqlite3 as sql
from . import var


class Databaser(object):
    def __init__(self):
        self.connection = sql.connect(var.FILEPATH_DATABASE)
        self.cursor = self.connection.cursor()

    def get_student(self, user_id):
        self.cursor.execute(f"SELECT * FROM {var.DATABASE_STUDENTS_TABLE} WHERE user_id = ?", (user_id,))
        return self.cursor.fetchone()

    def new_student(self, user_id, name, surname):
        self.cursor.execute(f"INSERT INTO {var.DATABASE_STUDENTS_TABLE} (user_id, name, surname) VALUES (?, ?, ?)", (user_id, name, surname))  # plz, don't do SQL injection on me :(
        self.connection.commit()

    def edit_student(self, user_id, attribute, value):
        self.cursor.execute(f"UPDATE {var.DATABASE_STUDENTS_TABLE} SET {attribute} = ? WHERE user_id = ?", (attribute, value, user_id))
