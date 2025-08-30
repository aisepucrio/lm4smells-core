import ollama
from abc import ABC, abstractmethod
from infrastructure.config.settings import settings
from application.dtos.message_operation_input import MessageOperationInput


class LMBaseService(ABC):
    def __init__(self):
        self.client = ollama.Client(host=settings.lm_ollama_host)

    @abstractmethod
    def send_message(self, type: MessageOperationInput):
        pass
