from infrastructure.repositories.ischedule_status_repository import IScheduleStatusRepository
from infrastructure.repositories.schedule_status_repository import ScheduleStatusRepository
from typing import Callable, Any, Tuple, List


class ScheduleStatusOperationUseCase:
    def __init__(self):
        self.repository: IScheduleStatusRepository = ScheduleStatusRepository()

    def execute(self, task_id: List[str]):
        return self.repository.get_schedule_status(task_id)
