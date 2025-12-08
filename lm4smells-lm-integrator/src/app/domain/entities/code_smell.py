from dataclasses import dataclass
from typing import Dict, Optional


class CodeSmell:
    def __init__(self, task_id: str, smell_type: str, explanation: str, file_name: str, model: str, 
                    programming_language: str, class_name: Optional[str], 
                    method_name: Optional[str], analyse_type: str,
                    code: str, prompt_type: str, prompt: str, 
                    is_composite_prompt: bool, code_metric: Dict):
        self.task_id = task_id
        self.smell_type = smell_type
        self.explanation = explanation
        self.file_name = file_name
        self.model = model
        self.programming_language = programming_language
        self.class_name = class_name
        self.method_name = method_name
        self.analyse_type = analyse_type
        self.code = code
        self.prompt_type = prompt_type
        self.prompt = prompt
        self.is_composite_prompt = is_composite_prompt
        self.code_metric = code_metric
