from modules import var
import logging

file_handler = logging.FileHandler(var.FILEPATH_LOG)
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(logging.Formatter('%(levelname)s;%(asctime)s;%(name)s;%(threadName)s;%(message)s'))
logging.getLogger().addHandler(file_handler)
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.ERROR)
stream_handler.setFormatter(logging.Formatter('%(levelname)s\t%(asctime)s\t%(name)s\t%(threadName)s\t%(message)s'))
logging.getLogger().addHandler(stream_handler)

from modules.ghislieribot import GhislieriBot


def main():
    gb = GhislieriBot()
    gb.run()


if __name__ == '__main__':
    main()
