class MessageOperationOutput:
    def __init__(self, file_name: str, programming_language: str, lineno: int, 
                 code_metric: dict, code: str, prompt_type: str, prompt: str,
                 model: str, is_composite_prompt: bool, analyse_type: str, 
                 class_name: str = None, method_name: str = None):
        self.file_name = file_name
        self.programming_language = programming_language
        self.lineno = lineno
        self.class_name = class_name
        self.method_name = method_name
        self.code_metric = code_metric
        self.code = code
        self.prompt_type = prompt_type
        self.analyse_type = analyse_type
        self.prompt = prompt
        self.model = model
        self.is_composite_prompt = is_composite_prompt


    @staticmethod
    def map_message_operation_output(input_message, extracted_result) -> "MessageOperationOutput":
        return MessageOperationOutput(
            file_name=extracted_result["file_name"],
            programming_language=extracted_result["programming_language"],
            lineno=extracted_result["lineno"],
            class_name=extracted_result.get("class_name"),
            method_name=extracted_result.get("method_name"),
            code_metric=extracted_result["code_metric"],
            code=extracted_result["code"],
            prompt_type=input_message.prompt_type,
            analyse_type=input_message.analyse_type,
            prompt=input_message.prompt,
            model=input_message.model,
            is_composite_prompt=input_message.is_composite_prompt,
        )
    
    
    def to_dict(self) -> dict:
        output = {
            "file_name": self.file_name,
            "programming_language": self.programming_language,
            "lineno": self.lineno,
            "code_metric": self.code_metric,
            "code": self.code,
            "prompt_type": self.prompt_type,
            "analyse_type": self.analyse_type,
            "prompt": self.prompt,
            "model": self.model,
            "is_composite_prompt": self.is_composite_prompt,
        }

        if self.class_name is not None:
            output["class_name"] = self.class_name
        if self.method_name is not None:
            output["method_name"] = self.method_name

        return output
