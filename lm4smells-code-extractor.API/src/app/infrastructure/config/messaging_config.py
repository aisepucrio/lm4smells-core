import pika
from infrastructure.config.settings import settings

class MessagingConfig:
    def __init__(self):
        self._host = settings.rabbit_host
        self._port = settings.rabbit_port
        self.username = settings.rabbit_username
        self.password = settings.rabbit_password

    def get_connection_parameters(self):
        return pika.ConnectionParameters(
            host=self._host, 
            port=self._port
        )
