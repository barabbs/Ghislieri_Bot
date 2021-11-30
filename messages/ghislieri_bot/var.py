import os, modules, datetime
from modules import formatting as fmt

# Directories
DATA_DIR = os.path.join(os.getcwd(), 'data')
CREDENTIALS_DIR = os.path.join(DATA_DIR, 'credentials')
DATABASES_DIR = os.path.join(DATA_DIR, 'databases')
FEEDBACK_DIR = os.path.join(DATA_DIR, 'feedback')
LOGS_DIR = os.path.join(DATA_DIR, 'logs')

# Files
DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'
FILEPATH_BOT_TOKEN = os.path.join(CREDENTIALS_DIR, 'ghislieri_bot_token.gbtk')
FILEPATH_DATABASE = os.path.join(DATABASES_DIR, 'database.gbdb')
FILEPATH_LOG = os.path.join(LOGS_DIR, f'ghislieri_bot {datetime.datetime.now().strftime(DATETIME_FORMAT)}.log')

# Bot
STUDENT_UPDATE_SECONDS_INTERVAL = 6

# Database
DATABASE_STUDENTS_TABLE = "students"
DATABASE_PERMISSIONS_TABLE = "permissions"

# Student
STUDENT_INFOS = {'name': "nome", 'surname': "cognome", 'email': "email"}
SESSION_TIMEOUT_SECONDS = 600

# About
ABOUT_BOT = f""":robot: {fmt.bold('Ghislieri Bot')} - version {modules.__version__}

Source code at https://github.com/barabbs/Ghislieri_Bot
{fmt.italic('Developed by Barabba')}
"""
