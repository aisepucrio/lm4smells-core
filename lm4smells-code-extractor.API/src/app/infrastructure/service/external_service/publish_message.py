from infrastructure.service.external_service.message_service import MessageService
from infrastructure.config.messaging_config import MessagingConfig


class PublishMessage:
    def __init__(self):
        self.messaging_config = MessagingConfig()
        self.message_service = MessageService(self.messaging_config)
    
    
    def publish_message(self, result: dict):
        self.message_service.send_message(result)