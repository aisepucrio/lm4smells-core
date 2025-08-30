from typing import Dict, Optional
from pydantic import BaseModel
from application.dtos.enums.prompt_type import PromptType
from application.dtos.enums.analyse_type import AnalyseType
from textwrap import dedent

class MessageOperationInput(BaseModel):
    model: str
    file_name: str
    programming_language: str
    class_name: Optional[str] = None
    method_name: Optional[str] = None
    analyse_type: str
    code: str
    prompt: str
    prompt_type: str
    is_composite_prompt: bool
    code_metric: Dict


    @classmethod
    def from_raw(cls, message):
        if isinstance(message, list):
            return [cls(**item) for item in message]
        elif isinstance(message, dict):
            return cls(**message)
        else:
            raise ValueError("Input must be a dictionary or a list of dictionaries.")
    

    def build_prompt(self) -> str:
        if self.prompt_type == PromptType.zero_shot:
            return self._zero_shot_prompt()
        
        if self.prompt_type == PromptType.zero_shot_chain_of_thought:
            return self._cot_prompt()
    

    def _format_lm_result(self) -> str:
        match self.analyse_type:
            case AnalyseType.long_parameter_list.value:
                return dedent("""{{"smell_type":"long parameter list"}} OR {{"smell_type":"non-long parameter list"}}""")
            case AnalyseType.long_method.value:
                return dedent("""{{"smell_type":"long method"}} OR {{"smell_type":"non-long method"}}""")


    def _zero_shot_prompt(self) -> str:
        if self.is_composite_prompt:
            return dedent(f"""
                    {self.prompt}
                    Code: {self.code} 

                    Metrics: {self.code_metric} 
                            
                    return the result as one of the following JSONs: {self._format_lm_result()} AND {{"explanation":"your explication about this code"}}
                    """)
        else:
            return dedent(f"""
                    {self.prompt} 
                    Code: {self.code}

                    return the result as one of the following JSONs: {self._format_lm_result()} AND {{"explanation":"your explication about this code"}}
                    """)
    

    def _cot_prompt(self) -> str:
        if self.is_composite_prompt:
            return  dedent(f"""
                    {self.prompt}
                    Code: {self.code}

                    Metrics: {self.code_metric}

                    Let's think step by step.
                    
                    return the result as one of the following JSONs: {self._format_lm_result()} AND {{"explanation":"your explication about this code"}}
                    """)
        else:
            return dedent(f"""
                    {self.prompt}
                    Code: {self.code}
                    
                    Let's think step by step.
                   
                    return the result as one of the following JSONs: {self._format_lm_result()} AND {{"explanation":"your explication about this code"}}
                    """)

