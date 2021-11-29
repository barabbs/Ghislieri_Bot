import os

# Directories
DATA_DIR = os.path.join(os.getcwd(), 'data')
CREDENTIALS_DIR = os.path.join(DATA_DIR, 'credentials')
DATABASES_DIR = os.path.join(DATA_DIR, 'databases')

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
