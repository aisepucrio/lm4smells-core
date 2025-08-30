from infrastructure.config.messaging_config import MessagingConfig
from infrastructure.external_service.message_service import MessageService


class ConsumeMessage:
    def __init__(self):
        self.messaging_config = MessagingConfig()
        self.message_service = MessageService(self.messaging_config)
        
    def get_message(self, callback):
        self.message_service.consume_message(callback)

