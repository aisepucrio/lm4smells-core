from application.dtos.request.ast_operation_input import ASTOperationInput
import threading
from infrastructure.modules.smells.ast.smells import Smells
from infrastructure.repositories.ismell_repository import ISmellRepository
from infrastructure.repositories.smell_repository import SmellRepository
from infrastructure.repositories.ischedule_status_repository import IScheduleStatusRepository
from infrastructure.repositories.schedule_status_repository import ScheduleStatusRepository
from infrastructure.service.schedule.enums.task_status import TaskStatus
from dataclasses import asdict
from application.dtos.enums.analyse_type import AnalyseType
from application.dtos.enums.approach import Approach


class ASTOperationUseCase:
    def __init__(self):
        self.smells = Smells()
        self.repository: ISmellRepository = SmellRepository()
        self.schedule_repository: IScheduleStatusRepository = ScheduleStatusRepository()

    def ast_based_code_classification_use_case(self, input: ASTOperationInput, cancel_event: threading.Event):
        self.schedule_repository.save_schedule_status(input.task_id, TaskStatus.RUNNING.value, Approach.AST.value)

        smell_result = self.__choose_smell_type(input)

        if not smell_result:
            print("No smells detected, terminating the process.")
            self.schedule_repository.save_schedule_status(input.task_id, TaskStatus.ERROR.value, Approach.AST.value)
            return

        for s in smell_result:
            if cancel_event.is_set():
                print("Task was cancelled")
                self.schedule_repository.save_schedule_status(input.task_id, TaskStatus.CANCELED.value, Approach.AST.value)
                return
            self.repository.save_all(s)
            self.schedule_repository.save_schedule_status(input.task_id, TaskStatus.COMPLETED.value, Approach.AST.value)
        print("AST-based code classification completed.")

    def __choose_smell_type(self, input: ASTOperationInput):
        if input.analyse_type == AnalyseType.long_parameter_list:
            return self.smells.long_parameter_list(input.task_id, input.file_contents, input.file_names)

        elif input.analyse_type == AnalyseType.long_method:
            return self.smells.long_method(input.task_id, input.file_contents, input.file_names)

        elif input.analyse_type == AnalyseType.large_class:
            return self.smells.large_class(input.task_id, input.file_contents, input.file_names)

        elif input.analyse_type == AnalyseType.data_class:
            return self.smells.data_class(input.task_id, input.file_contents[0], input.file_names[0])

        elif input.analyse_type == AnalyseType.lazy_class:
            return self.smells.lazy_class(input.task_id, input.file_contents[0], input.file_names[0])

        elif input.analyse_type == AnalyseType.magic_numbers:
            return self.smells.magic_numbers(input.task_id, input.file_contents[0], input.file_names[0])

        else:
            raise ValueError(f"Unsupported analysis type: {input.analyse_type}")


