from application.dtos.message_operation_input import MessageOperationInput
from application.usecase.lm_operation_usecase import LMOperationUseCase
from infrastructure.external_service.consume_message import ConsumeMessage


def process_message(message):
    message_input = MessageOperationInput.from_raw(message)
    
    gemma_service = LMOperationUseCase()
    gemma_service.lm_operation_use_case(message_input)

    if "error" in message:
        raise ValueError("Error processing the message.")


def main():    
    consume = ConsumeMessage()
    consume.get_message(process_message)

if __name__ == "__main__":
    main()
