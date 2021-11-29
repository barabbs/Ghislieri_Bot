from modules import basemessages as bmsg
from . import var

class AboutMessage(bmsg.BackMessage):
    TITLE = f":information: Info"
    TEXT = var.ABOUT_BOT
