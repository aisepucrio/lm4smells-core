from dataclasses import dataclass

@dataclass(frozen=True)
class UserOperationInput:
    task_id: str
    approach: str