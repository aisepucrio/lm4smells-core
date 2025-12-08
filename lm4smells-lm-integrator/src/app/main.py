from application.dtos.message_operation_input import MessageOperationInput
from application.usecase.lm_operation_usecase import LMOperationUseCase
from infrastructure.external_service.consume_message import ConsumeMessage
from infrastructure.repository.ischedule_status_repository import IScheduleStatusRepository
from infrastructure.repository.schedule_status_repository import ScheduleStatusRepository


class MainProcessor:
    def __init__(self):
        self.schedule_status_repository: IScheduleStatusRepository = ScheduleStatusRepository()

    def _mark_schedule_as_done(self, task_id: str, status: str):
        if status == "task_done":
            self.schedule_status_repository.update_schedule_status(task_id, status)
            return True
        return False


    def process_message(self, message):

        if self._mark_schedule_as_done(message.get("task_id"), message.get("type")):
            return

        try:
            message_input = MessageOperationInput.from_raw(message)
            
            lm_use_case = LMOperationUseCase()
            lm_use_case.lm_operation_use_case(message_input)

            if "error" in message:
                raise ValueError("Error processing the message.")
        
        except Exception as e:
            print(f"[ERROR] An error occurred while processing the message: {e}")
            raise e


def main():    
    consume = ConsumeMessage()
    main_processor = MainProcessor()
    consume.get_message(main_processor.process_message)

if __name__ == "__main__":
    main()
