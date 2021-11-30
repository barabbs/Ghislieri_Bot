from modules import utility as utl
from modules import var
import logging

logger = logging.getLogger()
file_handler = logging.FileHandler(var.FILEPATH_LOG)
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(logging.Formatter('%(levelname)s;%(asctime)s;%(name)s;%(threadName)s;%(message)s'))
logger.addHandler(file_handler)
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.ERROR)
stream_handler.setFormatter(logging.Formatter('%(levelname)s\t%(asctime)s\t%(name)s\t%(threadName)s\t%(message)s'))
logger.addHandler(stream_handler)

from modules.ghislieribot import GhislieriBot


def main():
    try:
        gb = GhislieriBot()
        gb.run()
    except Exception as e:
        logger.critical(f"Critical error while running GhislieriBot: {e}")
        utl.log_error(e, severity="critical")


if __name__ == '__main__':
    main()
