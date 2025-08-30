from abc import ABC, abstractmethod
from domain.entities.code_smell import CodeSmell

class ICodeSmellsRepository(ABC):
    @abstractmethod
    def persist_lm_result(self, code_smell: CodeSmell):
        pass