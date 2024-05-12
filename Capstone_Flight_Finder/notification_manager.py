from twilio.rest import Client
import os

class NotificationManager:
    def __init__(self):
        self._account_sid = os.environ['ENV_TWILIO_SID']
        self._auth_token = os.environ['ENV_TWILIO_TOKEN']
        self.number = '+18289002723'
        self._client = Client(self._account_sid, self._auth_token)

    def send_msg(self, msg):
        message = self._client.messages.create(
            body=msg,
            from_=self.number,
            to=os.environ['ENV_NUMBER']
        )


if __name__ == '__main__':
    msg_sender = NotificationManager()
    msg_sender.send_msg("Hola")
