from modules import basemessages as bmsg
from .feedback import FeedbackMessage
from .about import AboutMessage


class MainMessage(bmsg.BackMessage):
    TITLE = ":wrench: Impostazioni"
    TEXT = TITLE
    BUTTONS = [[("feedback", FeedbackMessage.TITLE, bmsg.get_new_message_answer(FeedbackMessage)), ],
               [("about", AboutMessage.TITLE, bmsg.get_new_message_answer(AboutMessage)), ],
               ]
