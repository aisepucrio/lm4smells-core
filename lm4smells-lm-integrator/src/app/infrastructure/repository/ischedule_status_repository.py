from abc import ABC, abstractmethod

class IScheduleStatusRepository(ABC):
    @abstractmethod
    def update_schedule_status(self, task_id: str, status: str):
        pass