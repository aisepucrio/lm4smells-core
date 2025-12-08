from typing import List
import threading
from fastapi import FastAPI, File, UploadFile, Form, Query
from application.usecase.message_operation_use_case import MessageOperationUseCase
from application.usecase.ast_operation_use_case import ASTOperationUseCase
from application.usecase.ml_operation_use_case import MLOperationUseCase
from application.usecase.dl_operation_use_case import DLOperationUseCase
from application.dtos.request.ml_operation_input import MLOperationInput
from application.dtos.request.dl_operation_input import DLOperationInput
from application.usecase.handle_codes_use_case import HandleCodesUseCase
from application.usecase.schedule_status_operation_use_case import ScheduleStatusOperationUseCase

from application.dtos.request.message_operation_input import MessageOperationInput
from application.dtos.request.ast_operation_input import ASTOperationInput
from application.dtos.request.user_operation_input import UserOperationInput
from application.dtos.enums.lm_models import LMModels
from application.dtos.enums.analyse_type import AnalyseType
from application.dtos.enums.extract_type import ExtractType
from application.dtos.enums.prompt_type import PromptType
from application.dtos.enums.smell_definition import SmellDefinition
from application.dtos.enums.ml_model import MLModel
from application.dtos.enums.dl_model import DLModel
from application.dtos.enums.approach import Approach

from fastapi.middleware.cors import CORSMiddleware
from uuid import uuid4
from application.usecase.handle_ml_codes_use_case import HandleMlCodesUseCase
from application.usecase.handle_dl_codes_use_case import HandleDlCodesUseCase
from infrastructure.service.schedule.task_manager import TaskManager


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

task_manager = TaskManager()


@app.post("/api/schedule/lm", summary="Classify code using an LM-based approach", tags=["Schedule"])
async def extract_code(is_composite_prompt: bool = Form(..., description="Indicate if you want to create a prompt composed of code + metrics."),
                       model: LMModels = Form(..., description="Indicate which LM model you would like to be processed."),
                      #prompt: str = Form(..., description="Message you would like to send to the model."),
                       prompt_type: PromptType = Form(..., description="Indicate the prompt type to process the message."),
                       analyse_type: AnalyseType = Form(..., description="Indicates the type of code smell: 1 for large Class - 2 for long Method - 3 for long parameter list."), 
                       extract_type: ExtractType = Form(..., description="Indicate the type of extraction you want to perform: 1 for Class or 2 for Method."),
                       files: List[UploadFile] = File(..., description="Specify the file you want to extract.")):
 
    
    task_id = str(uuid4())

    input = await MessageOperationInput.process_files(
        is_composite_prompt=is_composite_prompt,
        analyse_type=analyse_type,
        extract_type=extract_type,
        prompt_type=prompt_type,
        prompt="",
        model=model,
        files=files,
        task_id=task_id
    )

    task_manager.schedule(
        task_id=task_id,
        use_case=MessageOperationUseCase().create_message_use_case,
        use_case_args=(input,)
    )

    return {"status": "Scheduled", "task_id": task_id, "approach": "lm"}


@app.post("/api/schedule/ast", summary="Classify code using an AST-based approach", tags=["Schedule"])
async def classify_code_with_ast(
    extract_type: ExtractType = Form(..., description="Indicate the type of extraction you want to perform: 1 for Class or 2 for Method."),
    analyse_type: AnalyseType = Form(..., description="Indicates the type of code smell: 1 for large Class - 2 for long Method - 3 for long parameter list."),
    #smell_definition: SmellDefinition = Form(..., description="Specify the code smell definition to be applied, based on the selected author."),
    files: List[UploadFile] = File(..., description="Specify the file you want to extract.")
    ):

    task_id = str(uuid4())

    input = await ASTOperationInput.process_files(
        extract_type=extract_type,
        analyse_type=analyse_type,
        #smell_definition=smell_definition,
        files=files,
        task_id=task_id
    )

    task_manager.schedule(
        task_id=task_id,
        use_case=ASTOperationUseCase().ast_based_code_classification_use_case,
        use_case_args=(input,)
    )

    return {"status": "Scheduled", "task_id": task_id, "approach": "ast"}

@app.post("/api/schedule/ml", summary="Classify code using a ML-based approach", tags=["Schedule"])
async def classify_code_with_ml(
    files: List[UploadFile] = File(..., description="Specify the file you want to extract."),
    extract_type: ExtractType = Form(..., description="Indicate the type of extraction you want to perform: 1 for Class or 2 for Method."),
    analyse_type: AnalyseType = Form(..., description="Indicates the type of code smell: 1 for large Class - 2 for long Method - 3 for long parameter list."),
    ml_model: MLModel = Form(..., description="Indicate which ML model you would like to be processed.")
    ):

    task_id = str(uuid4())

    input = await MLOperationInput.process_files(
        files=files,
        extract_type=extract_type,
        analyse_type=analyse_type,
        ml_model=ml_model,
        task_id=task_id
    )

    task_manager.schedule(
        task_id=task_id,
        use_case=MLOperationUseCase().ml_based_code_classification_use_case,
        use_case_args=(input,)
    )

    return {"status": "Scheduled", "task_id": task_id, "approach": "ml"}

@app.post("/api/schedule/dl", summary="Classify code using a DL-based approach", tags=["Schedule"])
async def classify_code_with_dl(
    files: List[UploadFile] = File(..., description="Specify the file you want to extract."),
    extract_type: ExtractType = Form(..., description="Indicate the type of extraction you want to perform: 1 for Class or 2 for Method."),
    analyse_type: AnalyseType = Form(..., description="Indicates the type of code smell: 1 for large Class - 2 for long Method - 3 for long parameter list."),
    dl_model: DLModel = Form(..., description="Indicate which DL model you would like to be processed.")
    ):

    task_id = str(uuid4())

    input = await DLOperationInput.process_files(
        files=files,
        extract_type=extract_type,
        analyse_type=analyse_type,
        dl_model=dl_model,
        task_id=task_id
    )

    task_manager.schedule(
        task_id=task_id,
        use_case=DLOperationUseCase().dl_based_code_classification_use_case,
        use_case_args=(input,)
    )

    return {"status": "Scheduled", "task_id": task_id, "approach": "dl"}


@app.get("/api/schedule/status", summary="Check the status of a scheduled AST classification task", tags=["Schedule"])
async def get_classification_status(task_id: List[str] = Query(..., description="The ID of the task to check")):
    return ScheduleStatusOperationUseCase().execute(task_id=task_id)


@app.post("/api/schedule/cancel", summary="Cancel a scheduled AST classification task", tags=["Schedule"])
async def cancel_classification(task_id: str = Form(..., description="The ID of the task to cancel")):
    return task_manager.cancel(task_id=task_id)


# Endpoints to return smell from database by user identification and approach
@app.get("/api/lm/codes", summary="Get LM code metrics", tags=["Code Smells"])
async def get_lm_code_metrics(task_id: str = Query(..., description="ID to retrieve LM codes")):
    return HandleCodesUseCase().execute(
        UserOperationInput(task_id=task_id, approach=Approach.LM)
    )

@app.get("/api/ast/codes", summary="Get code smells", tags=["Code Smells"])
async def get_ast_code_smells(task_id: str = Query(..., description="ID to retrieve AST codes")):
    return HandleCodesUseCase().execute(
        UserOperationInput(task_id=task_id, approach=Approach.AST)
    )

@app.get("/api/ml/codes", summary="Get ML code smells", tags=["Code Smells"])
async def get_ml_code_smells(task_id: str = Query(..., description="ID to retrieve ML codes")):
    return HandleCodesUseCase().execute(
        UserOperationInput(task_id=task_id, approach=Approach.ML)
    )

@app.get("/api/dl/codes", summary="Get DL code smells", tags=["Code Smells"])
async def get_dl_code_smells(task_id: str = Query(..., description="ID to retrieve DL codes")):
    return HandleCodesUseCase().execute(
        UserOperationInput(task_id=task_id, approach=Approach.DL)
    )



# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)