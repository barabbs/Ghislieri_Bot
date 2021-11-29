from modules import basemessages as bmsg
from datetime import datetime
import os
from . import var


class ThankYouMessage(bmsg.NotificationMessage):
    TEXT = "Grazie per la segnalazione! :grinning_face_with_smiling_eyes:"


class FeedbackMessage(bmsg.TextMessage):
    TITLE = f":envelope: Segnalazioni e Suggerimenti"
    TEXT = "Che problema hai riscontrato?\nChe suggerimento hai per migliorare il bot?"
    TEXT_ANSWER = bmsg.get_new_message_answer(ThankYouMessage)

    def get_answer_text(self, text, student):
        time = datetime.now().strftime(var.DATETIME_FORMAT)
        with open(os.path.join(var.FEEDBACK_DIR, f"{student.user_id}_{time}.gbfb"), 'w', encoding='utf-8') as f:
            f.write(f"name={student.get_info('name')}\nsurname={student.get_info('surname')}\nuser_id={student.user_id}\ntime={time}\n\n{text}")
        return super(FeedbackMessage, self).get_answer_text(text, student)