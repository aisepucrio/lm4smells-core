import threading
from typing import List, Dict

from application.dtos.request.dl_operation_input import DLOperationInput
from application.dtos.enums.extract_type import ExtractType
from application.dtos.enums.approach import Approach
from infrastructure.repositories.dl_classification_repository import DLClassificationRepository
from infrastructure.repositories.schedule_status_repository import ScheduleStatusRepository
from infrastructure.service.schedule.enums.task_status import TaskStatus
from infrastructure.modules.smells.dl.dl_classifier import DLClassifier
from infrastructure.service.extract_codes.class_extractor import ClassExtractor
from infrastructure.service.extract_codes.method_extractor import MethodExtractor


class DLOperationUseCase:
    def __init__(self):
        self.dl_classifier = DLClassifier()
        self.repository = DLClassificationRepository()
        self.schedule_repository = ScheduleStatusRepository()
        self.class_extractor = ClassExtractor()
        self.method_extractor = MethodExtractor()

    def dl_based_code_classification_use_case(
        self,
        input: DLOperationInput,
        cancel_event: threading.Event,
    ):

        self.schedule_repository.save_schedule_status(input.task_id, TaskStatus.RUNNING.value, Approach.DL.value)

        extractor = self.__get_extractor(input.extract_type)
        if not extractor:
            raise ValueError(f"Invalid extract_type: {input.extract_type}")

        print("The code extraction process has started")
        result = extractor.extract(input.respective_codes)
        print("The code extraction process has finished")

        if not result:
            print("No code extracted, terminating the process.")
            self.schedule_repository.save_schedule_status(input.task_id, TaskStatus.ERROR.value, Approach.DL.value)
            return

        print("Mapping the extracted code metrics to the DL model input format")
        input.map_metrics_to_dl_input(result)
        print("Mapping the extracted code metrics to the DL model input format completed.")

        print("The DL-based code classification process has started")
        classifications = self.__classify_with_dl_model(input, result)
        print("The DL-based code classification process has finished")

        for c in classifications:
            if cancel_event.is_set():
                print("Task was cancelled")
                self.schedule_repository.save_schedule_status(input.task_id, TaskStatus.CANCELED.value, Approach.DL.value)
                return
            self.repository.save_all(c)
            self.schedule_repository.save_schedule_status(input.task_id, TaskStatus.COMPLETED.value, Approach.DL.value)
        print("DL-based code classification completed.")

    def __classify_with_dl_model(
        self,
        input: DLOperationInput,
        extraction_results: List[Dict],
    ):
        if input.extract_type == ExtractType.classes:
            return self.dl_classifier.classify_classes(input.task_id, extraction_results, input.dl_model)
        elif input.extract_type == ExtractType.methods:
            return self.dl_classifier.classify_methods(input.task_id, extraction_results, input.dl_model)
        else:
            raise ValueError(f"Unsupported extraction type: {input.extract_type}")

    def __get_extractor(self, extract_type: ExtractType):
        if extract_type == ExtractType.classes:
            return self.class_extractor
        if extract_type == ExtractType.methods:
            return self.method_extractor
        return None
