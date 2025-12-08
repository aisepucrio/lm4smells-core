from domain.entities.code_smell import CodeSmell

class CodeSmellMapper:
    @staticmethod
    def from_lm_response(message_input, lm_result) -> CodeSmell:
        return CodeSmell(
            task_id=message_input.task_id,
            smell_type=lm_result.smell_type,
            explanation=lm_result.explanation,
            file_name=message_input.file_name,
            model=message_input.model,
            programming_language=message_input.programming_language,
            class_name=message_input.class_name,
            method_name=message_input.method_name, 
            analyse_type=message_input.analyse_type, 
            code=message_input.code, 
            prompt_type=message_input.prompt_type, 
            prompt=message_input.build_prompt(), 
            is_composite_prompt=message_input.is_composite_prompt, 
            code_metric=message_input.code_metric 
        )
