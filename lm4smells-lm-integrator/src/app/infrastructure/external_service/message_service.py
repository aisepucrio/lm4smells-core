from infrastructure.config.messaging_config import MessagingConfig
from infrastructure.config.settings import settings
from threading import Thread
from queue import Queue, Empty
import pika
import json


class MessageService:
    def __init__(self, config: MessagingConfig):
        self.config = config
        self.queue = settings.rabbit_queue
        self.exchange = settings.rabbit_exchange
        self.routing_key = settings.rabbit_routing_key
        self.local_queue = Queue()
        self.worker_thread = None
        self.batch_size = settings.rabbit_batch_size
    
    
    def consume_message(self, callback):
        connection = pika.BlockingConnection(self.config.get_connection_parameters())
        channel = connection.channel()
        channel.queue_declare(queue=self.queue, durable=True)

        self.worker_thread = Thread(target=self._process_local_queue, args=(callback,), daemon=True)
        self.worker_thread.start()

        channel.basic_qos(prefetch_count=self.batch_size)
        channel.basic_consume(
            queue=self.queue,
            on_message_callback=lambda ch, method, properties, body: self._consume_to_local_queue(ch, method, body),
            auto_ack=False
        )

        print(f"[*] Waiting for messages in the queue '{self.queue}'. Press CTRL+C to exit.")
        try:
            channel.start_consuming()
        except KeyboardInterrupt:
            print("\n[WARNING] Consumption interrupted by the user.")
            connection.close()
    
    def _consume_to_local_queue(self, channel, method, body):

        if self.local_queue.qsize() >= self.batch_size:
            print("[INFO] Local queue is full. Waiting for processing...")
            channel.basic_nack(delivery_tag=method.delivery_tag, requeue=True)
            return

        try:
            message = json.loads(body)
            self.local_queue.put((message, channel, method.delivery_tag))
            print(f"[INFO] Message added to the local queue")
        except Exception as e:
            print(f"[ERROR] Error consuming message: {body}. Error: {e}")
            channel.basic_nack(delivery_tag=method.delivery_tag, requeue=False)


    def _process_local_queue(self, callback):
        while True:
            try:
                message, channel, delivery_tag = self.local_queue.get(timeout=1)

                callback(message)
                print(f"[INFO] Message processed")

                channel.basic_ack(delivery_tag=delivery_tag)
            except Empty:
                pass
            except Exception as e:
                print(f"[ERROR] Error processing message from the local queue: {e}")
            finally:
                if not self.local_queue.empty():
                    self.local_queue.task_done()


