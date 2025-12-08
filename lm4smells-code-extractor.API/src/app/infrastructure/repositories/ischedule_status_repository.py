from abc import ABC, abstractmethod
from typing import List

class IScheduleStatusRepository(ABC):
    @abstractmethod
    def get_schedule_status(self, task_id: List[str]):
        pass

    @abstractmethod
    def save_schedule_status(self, task_id: str, status: str, task_type: str):
        pass