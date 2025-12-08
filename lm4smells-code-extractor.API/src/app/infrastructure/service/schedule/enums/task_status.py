from enum import Enum

class TaskStatus(Enum):
    SCHEDULED = "Scheduled"
    RUNNING = "Running"
    COMPLETED = "Completed"
    CANCELED = "Canceled"
    ERROR = "Error"
