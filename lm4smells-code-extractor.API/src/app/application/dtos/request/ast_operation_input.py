from typing import List
from fastapi import UploadFile

class ASTOperationInput:
    def __init__(self, file_contents, file_names, extract_type, analyse_type, task_id):
        self.file_contents = file_contents
        self.file_names = file_names
        self.extract_type = extract_type
        self.analyse_type = analyse_type
        #self.smell_definition = smell_definition
        self.task_id = task_id
    
    @classmethod
    async def process_files(
        cls,
        extract_type,
        analyse_type,
        #smell_definition,
        files: List[UploadFile],
        task_id
    ):
        raw_file_content = [await file.read() for file in files]
        decoded_file_content = [content.decode("utf-8") for content in raw_file_content]
        file_names = [file.filename for file in files]

        return cls(
            file_contents=decoded_file_content,
            file_names=file_names,
            extract_type=extract_type,
            analyse_type=analyse_type,
            #smell_definition=smell_definition,
            task_id=task_id
        )