from application.dtos.request.message_operation_input import MessageOperationInput
from infrastructure.service.extract_codes.class_extractor import ClassExtractor
from infrastructure.service.extract_codes.method_extractor import MethodExtractor
from infrastructure.service.external_service.publish_message import PublishMessage
from application.dtos.response.message_operation_output import MessageOperationOutput
from infrastructure.repositories.ischedule_status_repository import IScheduleStatusRepository
from infrastructure.repositories.schedule_status_repository import ScheduleStatusRepository
from typing import List
import threading
from application.dtos.enums.approach import Approach
from infrastructure.service.schedule.enums.task_status import TaskStatus


class MessageOperationUseCase:
    def __init__(self):
        self.extractor_class = ClassExtractor()
        self.extractor_method = MethodExtractor()
        self.schedule_repository: IScheduleStatusRepository = ScheduleStatusRepository()
        self.publish = PublishMessage()


    def create_message_use_case(self, message: MessageOperationInput, cancel_event: threading.Event):
        try:
            self.schedule_repository.save_schedule_status(message.task_id, TaskStatus.RUNNING.value, Approach.LM.value)
            print("The task status Running has been saved successfully")


            extractor = self._get_extractor(message.extract_type)
            if not extractor:
                raise ValueError(f"Invalid extract_type: {message.extract_type}")
            
            print("The code extraction process has started")
            result = extractor.extract(message.respective_codes)
            print("The code extraction process has finished")

            for idx, extract_result in enumerate(result, start=1):
                if cancel_event.is_set():
                    print("Task was cancelled")
                    self.schedule_repository.save_schedule_status(message.task_id, TaskStatus.CANCELED.value, Approach.LM.value)
                    return

                print("The process of putting messages into the queue started")
                publish = self._publish_item(extract_result, message)
                print("The process of putting messages into the queue finished.")

            self._notification_finalize_process(message)
            print("The process of creating the message was successful")


        except Exception as e:
            print(f"The process of creating the message failed: {e}")


    def _get_extractor(self, extract_type: int):
        if extract_type == 1:
            return self.extractor_class
        elif extract_type == 2:
            return self.extractor_method
        return None


    def _publish_item(self, extract_result: dict, message: MessageOperationInput):
        map_operation_output_response = MessageOperationOutput.map_message_operation_output(message, extract_result)
        self.publish.publish_message(map_operation_output_response.to_dict())


    def _notification_finalize_process(self, message: MessageOperationInput):
        try:
            done = {
                "type": "task_done",
                "task_id": message.task_id
            }
            self.publish.publish_message(done)
            print("The finalize process message was sent successfully")
        except Exception as e:
            print(f"The process of sending the finalize message failed: {e}")
