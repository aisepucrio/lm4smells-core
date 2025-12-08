from typing import Dict, Optional
from pydantic import BaseModel
from application.dtos.enums.prompt_type import PromptType
from application.dtos.enums.analyse_type import AnalyseType
from textwrap import dedent

class MessageOperationInput(BaseModel):
    task_id: str
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

    def _header_zero_shot_prompt(self) -> str:
        match self.analyse_type:
            case AnalyseType.long_parameter_list.value:
                return dedent(f"""Classify the code as a {AnalyseType.long_parameter_list.value} or a non-{AnalyseType.long_parameter_list.value}""")
            case AnalyseType.long_method.value:
                return dedent(f"""Classify the code as a {AnalyseType.long_method.value} or a non-{AnalyseType.long_method.value}""")

    def _zero_shot_prompt(self) -> str:
        if self.is_composite_prompt:
            return dedent(f"""
                    {self._header_zero_shot_prompt()}

                    Code: {self.code} 

                    Metrics: {self.code_metric} 
                            
                    return the result as one of the following JSONs: {self._format_lm_result()} AND {{"explanation":"your explication about this code"}}
                    """)
        else:
            return dedent(f"""
                    {self._header_zero_shot_prompt()} 

                    Code: {self.code}

                    return the result as one of the following JSONs: {self._format_lm_result()} AND {{"explanation":"your explication about this code"}}
                    """)
    

    def _header_cot_prompt(self) -> str:
        match self.analyse_type:
            case AnalyseType.long_parameter_list.value:
                return dedent(f"""
                    Methods with a long list of parameters make the code difficult to understand, modify, and reuse. When a method receives too many parameters, it may indicate that it 
                    is overly coupled to multiple parts of the system, making calls confusing and hard to remember. This issue also complicates refactoring, as any change to the 
                    parameters requires modifying all function calls. Additionally, methods with many parameters often receive groups of variables that could be encapsulated into a 
                    single object, avoiding repetition and making the code more organized. This code smell may also be a symptom that the function is handling multiple 
                    responsibilities, making it harder to test and maintain.

                    Based on these characteristics, the provided code may exhibit signs of this problem if it has an extensive signature, with parameters that frequently appear 
                    together or if there are many arguments derived from the same object. This may indicate the need for refactoring, such as introducing data classes, parameter 
                    objects, or extracting responsibilities into helper methods.

                    Does the provided code show signs of this problem?
                """)
            case AnalyseType.long_method.value:
                return dedent(f"""
                    Long methods make code difficult to understand, test, and maintain. When a method grows too large, it can exhibit high complexity, 
                    excessive conditional statements, nested loops, and multiple responsibilities, violating the Single Responsibility Principle (SRP).
                    Additionally, long methods often mix different levels of abstraction, making the code harder to read and reuse. 
                    Changes in this type of code are more prone to errors, affecting multiple parts of the system. Based on these characteristics, 
                    the provided code may show signs of this code smell if it has too many lines, a high level of coupling, excessive parameters or local variables, 
                    and performs multiple operations that could be extracted into smaller, more cohesive functions. Does the provided code exhibit signs of a long method?
                """)


    def _cot_prompt(self) -> str:
        if self.is_composite_prompt:
            return  dedent(f"""
                    {self._header_cot_prompt()}
                    Code: {self.code}

                    Metrics: {self.code_metric}

                    Let's think step by step.
                    
                    return the result as one of the following JSONs: {self._format_lm_result()} AND {{"explanation":"your explication about this code"}}
                    """)
        else:
            return dedent(f"""
                    {self._header_cot_prompt()}
                    Code: {self.code}
                    
                    Let's think step by step.
                   
                    return the result as one of the following JSONs: {self._format_lm_result()} AND {{"explanation":"your explication about this code"}}
                    """)

