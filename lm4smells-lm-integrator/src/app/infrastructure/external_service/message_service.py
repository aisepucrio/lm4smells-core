from infrastructure.config.messaging_config import MessagingConfig
from infrastructure.config.settings import settings
from threading import Thread
from queue import Queue, Empty
import pika
import json
import time

class MessageService:
    def __init__(self, config: MessagingConfig):
        self.config = config
        self.queue = settings.rabbit_queue
        self.exchange = settings.rabbit_exchange
        self.routing_key = settings.rabbit_routing_key
        self.batch_size = settings.rabbit_batch_size

        self._work_q = Queue(maxsize=self.batch_size)
        self._result_q = Queue(maxsize=self.batch_size)

        self._worker = None
        self._stopping = False

    def consume_message(self, callback):
        channel = self._connect_with_retry()
        channel.queue_declare(queue=self.queue, durable=True)
        channel.basic_qos(prefetch_count=self.batch_size)

        self._worker = Thread(
            target=self._worker_loop,
            args=(callback,),
            daemon=True
        )
        self._worker.start()

        print(f"[*] Waiting for messages in the queue '{self.queue}'. Press CTRL+C to exit.")

        def on_message(ch, method, properties, body):
            try:
                msg = json.loads(body)
            except Exception as e:
                print(f"[ERROR] Invalid JSON: {e}. NACK (no requeue). body={body!r}")
                ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
                return

            try:
                self._work_q.put((method.delivery_tag, msg), timeout=5)
            except Exception:
                print("[WARN] Work queue full. Requeue message.")
                ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)
                return

            self._drain_results_nonblocking(ch)

        channel.basic_consume(queue=self.queue, on_message_callback=on_message, auto_ack=False)

        try:
            while not self._stopping:
                channel.connection.process_data_events(time_limit=1.0)
                self._drain_results_nonblocking(channel)
        except KeyboardInterrupt:
            print("\n[WARNING] Consumption interrupted by the user.")
        finally:
            self._stopping = True
            try:
                channel.close()
            except Exception:
                pass


    def _connect_with_retry(self, attempts: int = 10, delay: float = 2.0):
        for i in range(1, attempts + 1):
            try:
                params = self.config.get_connection_parameters()
                conn = pika.BlockingConnection(params)
                ch = conn.channel()
                return ch
            except Exception as e:
                if i == attempts:
                    raise
                print(f"[WARN] RabbitMQ connect failed ({e}). Retry {i}/{attempts} in {delay}s...")
                time.sleep(delay)
                delay = min(delay * 1.5, 10)
        raise RuntimeError("unreachable")

    def _worker_loop(self, callback):
        while not self._stopping:
            try:
                delivery_tag, msg = self._work_q.get(timeout=1)
            except Empty:
                continue

            try:
                callback(msg)
                self._result_q.put(("ack", delivery_tag), timeout=3)
            except Exception as e:
                print(f"[ERROR] Error processing message from the local queue: {e}")
                try:
                    self._result_q.put(("nack", delivery_tag), timeout=3)
                except Exception:
                    print("[ERROR] Failed enqueue nack; message may be requeued later")
            finally:
                self._work_q.task_done()

    def _drain_results_nonblocking(self, ch):
        while True:
            try:
                action, delivery_tag = self._result_q.get_nowait()
            except Empty:
                break

            try:
                if action == "ack":
                    ch.basic_ack(delivery_tag=delivery_tag)
                else:
                    ch.basic_nack(delivery_tag=delivery_tag, requeue=True)
            except Exception as e:
                print(f"[ERROR] Channel error during {action} for tag {delivery_tag}: {e}")
            finally:
                self._result_q.task_done()
