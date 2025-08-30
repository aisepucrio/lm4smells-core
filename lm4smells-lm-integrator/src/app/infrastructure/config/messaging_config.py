from infrastructure.config.settings import settings
import pika 

class MessagingConfig:
    def __init__(self):
        self._host = settings.rabbit_host
        self._port = settings.rabbit_port
        self.username = settings.rabbit_username
        self.password = settings.rabbit_password
        self.virtual_host = settings.rabbit_virtual_host
        self.batch_size = settings.rabbit_batch_size

    def get_connection_parameters(self):
        return pika.ConnectionParameters(
            host=self._host, 
            port=self._port
        )
