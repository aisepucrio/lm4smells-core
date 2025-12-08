from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass(frozen=True)
class LMCode:
    id: str
    smell_type: str
    explanation: str
    file_name: str
    model: str
    programming_language: str
    class_name: Optional[str]
    method_name: Optional[str]
    analyse_type: str
    code: str
    prompt_type: str
    prompt: str
    is_composite_prompt: bool
    code_metric: str
    created_at: Optional[datetime]
