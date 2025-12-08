import threading
from typing import List, Dict

from application.dtos.request.ml_operation_input import MLOperationInput
from application.dtos.enums.extract_type import ExtractType
from application.dtos.enums.approach import Approach
from infrastructure.repositories.ml_classification_repository import MLClassificationRepository
from infrastructure.service.schedule.enums.task_status import TaskStatus
from infrastructure.modules.smells.ml.ml_classifier import MLClassifier
from infrastructure.service.extract_codes.class_extractor import ClassExtractor
from infrastructure.service.extract_codes.method_extractor import MethodExtractor
from infrastructure.repositories.schedule_status_repository import ScheduleStatusRepository

class MLOperationUseCase:
    def __init__(self):
        self.ml_classifier = MLClassifier()
        self.repository = MLClassificationRepository()
        self.schedule_repository = ScheduleStatusRepository()
        self.class_extractor = ClassExtractor()
        self.method_extractor = MethodExtractor()

    def ml_based_code_classification_use_case(
        self,
        input: MLOperationInput,
        cancel_event: threading.Event,
    ):

        self.schedule_repository.save_schedule_status(input.task_id, TaskStatus.RUNNING.value, Approach.ML.value)

        extractor = self.__get_extractor(input.extract_type)
        if not extractor:
            raise ValueError(f"Invalid extract_type: {input.extract_type}")

        print("The code extraction process has started")
        result = extractor.extract(input.respective_codes)
        print("The code extraction process has finished")

        if not result:
            print("No code extracted, terminating the process.")
            self.schedule_repository.save_schedule_status(input.task_id, TaskStatus.ERROR.value, Approach.ML.value)
            return

        print("Mapping the extracted code metrics to the ML model input format")
        input.map_metrics_to_ml_input(result)
        print("Mapping the extracted code metrics to the ML model input format completed.")

        print("The ML-based code classification process has started")
        classifications = self.__classify_with_ml_model(input, result)
        print("The ML-based code classification process has finished")

        for c in classifications:
            if cancel_event.is_set():
                print("Task was cancelled")
                self.schedule_repository.save_schedule_status(input.task_id, TaskStatus.CANCELED.value, Approach.ML.value)
                return
            self.repository.save_all(c)
            self.schedule_repository.save_schedule_status(input.task_id, TaskStatus.COMPLETED.value, Approach.ML.value)
        print("ML-based code classification completed.")


    def __classify_with_ml_model(
        self,
        input: MLOperationInput,
        extraction_results: List[Dict],
    ):
        if input.extract_type == ExtractType.classes:
            return self.ml_classifier.classify_classes(input.task_id, extraction_results, input.ml_model, input.analyse_type)
        elif input.extract_type == ExtractType.methods:
            return self.ml_classifier.classify_methods(input.task_id, extraction_results, input.ml_model, input.analyse_type)
        else:
            raise ValueError(f"Unsupported extraction type: {input.extract_type}")

    def __get_extractor(self, extract_type: ExtractType):
        if extract_type == ExtractType.classes:
            return self.class_extractor
        if extract_type == ExtractType.methods:
            return self.method_extractor
        return None
