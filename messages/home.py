from modules import basemessages as bmsg


class HomeMessage(bmsg.QueryMessage):
    TEXT = f":red_circle::yellow_circle: {bmsg.fmt.bold('Collegio Ghislieri')} :red_circle::yellow_circle:"


class WelcomeMessage(bmsg.NotificationMessage):
    TEXT = f"Benvenuto su Ghislieri Bot, il bot per i servizi del Collegio! :grinning_face_with_smiling_eyes:"
