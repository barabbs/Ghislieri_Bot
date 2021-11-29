import os
import modules

# Directories
DATA_DIR = os.path.join(os.getcwd(), 'data')
CREDENTIALS_DIR = os.path.join(DATA_DIR, 'credentials')
DATABASES_DIR = os.path.join(DATA_DIR, 'databases')
FEEDBACK_DIR = os.path.join(DATA_DIR, 'feedback')

# Files
FILEPATH_BOT_TOKEN = os.path.join(CREDENTIALS_DIR, 'ghislieri_bot_token.gbtk')
FILEPATH_DATABASE = os.path.join(DATABASES_DIR, 'database.gbdb')

# Bot
STUDENT_UPDATE_SECONDS_INTERVAL = 6

# Database
DATABASE_STUDENTS_TABLE = "students"
DATABASE_PERMISSIONS_TABLE = "permissions"

# Student
STUDENT_INFOS = ('name', 'surname', 'email')
SESSION_TIMEOUT_SECONDS = 600

# Feedback
DATETIME_FORMAT = '%Y-%m-%d_%H:%M:%S'

# About
ABOUT_BOT = f""":robot: Ghislieri Bot
version {modules.__version__}

Source code can be found at
https://github.com/barabbs/Ghislieri_Bot

Developed by Barabba"""
