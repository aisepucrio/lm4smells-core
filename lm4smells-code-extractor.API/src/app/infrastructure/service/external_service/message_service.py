from infrastructure.config.messaging_config import MessagingConfig
from infrastructure.config.settings import settings
import pika
import json


class MessageService:
    def __init__(self, config: MessagingConfig):
        self.config = config
        self.queue = settings.rabbit_queue
        self.exchange = settings.rabbit_exchange
        self.routing_key = settings.rabbit_routing_key


    def send_message(self, message: dict):
        connection = pika.BlockingConnection(self.config.get_connection_parameters())
        channel = connection.channel()
        channel.queue_declare(queue=self.queue, durable=True)

        channel.basic_publish(
            exchange=self.exchange,
            routing_key=self.routing_key,
            body=json.dumps(message),
            properties=pika.BasicProperties(
                delivery_mode=2,
            )
        )
        connection.close()

