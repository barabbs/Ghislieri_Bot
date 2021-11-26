from . import var


def get_bot_token():
    with open(var.FILEPATH_BOT_TOKEN, 'r') as token_file:
        return token_file.readline()
