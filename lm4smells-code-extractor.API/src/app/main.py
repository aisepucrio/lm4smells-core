from typing import List
from fastapi import FastAPI, File, UploadFile, Form
from application.usecase.message_operation_use_case import MessageOperationUseCase
from application.dtos.request.message_operation_input import MessageOperationInput
from application.dtos.enums.lm_models import LMModels
from application.dtos.enums.analyse_type import AnalyseType
from application.dtos.enums.extract_type import ExtractType
from application.dtos.enums.prompt_type import PromptType

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

message_operation_use_case_result = MessageOperationUseCase()


@app.post("/", summary="Extract code from uploaded files")
async def extract_code(is_composite_prompt: bool = Form(..., description="Indicate if you want to create a prompt composed of code + metrics."),
                       model: LMModels = Form(..., description="Indicate which LM model you would like to be processed."),
                       prompt: str = Form(..., description="Message you would like to send to the model."),
                       prompt_type: PromptType = Form(..., description="Indicate the prompt type to process the message."),
                       analyse_type: AnalyseType = Form(..., description="Indicates the type of code smell: 1 for large Class - 2 for long Method - 3 for long parameter list."), 
                       extract_type: ExtractType = Form(..., description="Indicate the type of extraction you want to perform: 1 for Class or 2 for Method."),
                       files: List[UploadFile] = File(..., description="Specify the file you want to extract.")):
 
    message = await MessageOperationInput.process_files( 
                                    is_composite_prompt=is_composite_prompt,
                                    analyse_type=analyse_type,
                                    extract_type=extract_type,
                                    prompt_type=prompt_type,
                                    prompt=prompt,
                                    model=model,
                                    files=files)
    
    result = message_operation_use_case_result.create_message_use_case(message)

    return result
