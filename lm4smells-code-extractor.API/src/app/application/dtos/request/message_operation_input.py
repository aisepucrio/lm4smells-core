from typing import List
from fastapi import UploadFile

class MessageOperationInput:
    def __init__(self, is_composite_prompt: bool, model: str, prompt: str, prompt_type: str, 
                 code: list, file_name: list, analyse_type: str, extract_type: int):
        self.is_composite_prompt = is_composite_prompt
        self.model = model.value
        self.prompt = prompt
        self.prompt_type = prompt_type.value
        self.code = code
        self.file_name = file_name
        self.analyse_type = analyse_type.value
        self.extract_type = extract_type.value
        self.programming_language = ["python"] * len(file_name)

    @property
    def respective_codes(self):
        return [{"file_name": fname, "code": fcode, "programming_language": planguage} 
                for fname, fcode, planguage in zip(self.file_name, self.code, self.programming_language)]
    

    @classmethod
    async def process_files(cls, is_composite_prompt: bool, model: str, prompt: str, prompt_type: str,
                         analyse_type: int, extract_type: int, files: List[UploadFile]):
        
        raw_file_content = [await file.read() for file in files]
        decoded_file_content = [content.decode("utf-8") for content in raw_file_content]
        file_names = [file.filename for file in files]

        return cls(
            is_composite_prompt=is_composite_prompt,
            model=model,
            prompt_type=prompt_type,
            prompt=prompt,
            analyse_type=analyse_type,
            extract_type=extract_type,
            code=decoded_file_content,
            file_name=file_names
        )
