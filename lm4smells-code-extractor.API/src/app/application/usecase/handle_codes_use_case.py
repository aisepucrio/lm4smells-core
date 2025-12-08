from infrastructure.repositories.smell_repository import SmellRepository
from infrastructure.repositories.ismell_repository import ISmellRepository
from application.dtos.request.user_operation_input import UserOperationInput
from application.dtos.enums.approach import Approach

class HandleCodesUseCase:
    def __init__(self):
        self.repository: ISmellRepository = SmellRepository()

    def execute(self, input: UserOperationInput):
        return self.__code_by_approach(input)

    def __code_by_approach(self, input: UserOperationInput):
        match input.approach:
            case Approach.LM: return self.repository.get_lm_codes_by_id(input.task_id)
            case Approach.ML: return self.repository.get_ml_codes_by_id(input.task_id)
            case Approach.DL: return self.repository.get_dl_codes_by_id(input.task_id)
            case Approach.AST: return self.repository.get_ast_codes_by_id(input.task_id)
            case _: raise ValueError(f"Invalid approach: {input.approach}")