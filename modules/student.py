from .databaser import Databaser
from . import var

STUDENTS_DATABASE = Databaser()


class Student(object):
    def __init__(self, user_id):
        self.user_id, self.name, self.surname, self.email = STUDENTS_DATABASE.get_student(user_id)
        # TODO: Add user permissions
