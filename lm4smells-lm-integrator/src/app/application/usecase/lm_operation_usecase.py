from infrastructure.external_service.lm_service import LMService
from application.dtos.message_operation_input import MessageOperationInput
from infrastructure.repository.code_smells_repository import CodeSmellsRepository
from infrastructure.repository.icode_smell_repository import ICodeSmellsRepository
from application.dtos.llm_gpt_models import LLMGPTModels
from application.dtos.slm_ollama_models import SLMOllamaModels
from application.mappers.code_smell_mapper import CodeSmellMapper


class LMOperationUseCase:
    def __init__(self):
        self.lm_service = LMService()
        self.repository: ICodeSmellsRepository = CodeSmellsRepository()

    def lm_operation_use_case(self, message_input: MessageOperationInput):
        try:
            print(f"[INFO] Processing a message in the {message_input.model} - file: {message_input.file_name}")
            lm_result = self._choose_model(message_input)

            print("[INFO] The mapping process has started")
            smell = CodeSmellMapper.from_lm_response(message_input, lm_result)

            print(f"[INFO] The persistence process for the {message_input.model} has started.")
            self.repository.persist_lm_result(smell)
            print(f"[INFO] The persistence process has ended.")

        except Exception as ex:
            print(f"[ERROR] An error occurred during {message_input.model} model response: {ex}")
            raise


    def _choose_model(self, message_input: MessageOperationInput):
        if message_input.model in LLMGPTModels._value2member_map_:
            return self.lm_service.send_message_gpt(message_input.model, message_input.build_prompt())
         
        if message_input.model in SLMOllamaModels._value2member_map_:
            return self.lm_service.send_message(message_input.model, message_input.build_prompt())


