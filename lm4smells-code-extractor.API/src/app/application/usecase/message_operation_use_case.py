from application.dtos.request.message_operation_input import MessageOperationInput
from infrastructure.service.extract_codes.class_extractor import ClassExtractor
from infrastructure.service.extract_codes.method_extractor import MethodExtractor
from infrastructure.service.external_service.publish_message import PublishMessage
from application.dtos.response.message_operation_output import MessageOperationOutput
from typing import List

class MessageOperationUseCase:
    def __init__(self):
        self.extractor_class = ClassExtractor()
        self.extractor_method = MethodExtractor()
        self.publish = PublishMessage()


    def create_message_use_case(self, message: MessageOperationInput):
        try:
            extractor = self._get_extractor(message.extract_type)
            if not extractor:
                raise ValueError(f"Invalid extract_type: {message.extract_type}")
            
            print("The code extraction process has started")
            result = extractor.extract(message.respective_codes)
            print("The code extraction process has finished")

            print("The process of putting messages into the queue started")
            client_response_message = self._process_and_publish(result, message)
            print(
                f"The process of putting messages into the queue finished. "
                f"{len(result)} codes extracted from {len(client_response_message)} published"
            )

            return client_response_message
        except Exception as e:
            print(f"The process of creating the message failed: {e}")


    def _get_extractor(self, extract_type: int):
        if extract_type == 1:
            return self.extractor_class
        elif extract_type == 2:
            return self.extractor_method
        return None


    def _process_and_publish(self, results: List[dict], message: MessageOperationInput):
        client_response_message = []
        for extract_result in results:
            map_operation_output_response = MessageOperationOutput.map_message_operation_output(
                message, extract_result
            )
            self.publish.publish_message(map_operation_output_response.to_dict())
            client_response_message.append(map_operation_output_response.to_dict())
        return client_response_message
    

