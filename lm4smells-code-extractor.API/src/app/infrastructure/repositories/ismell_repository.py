from abc import ABC, abstractmethod
from domain.entities.smell_occurrence import SmellOccurrence
from domain.entities.ml_classification import MLClassification
from domain.entities.dl_classification import DLClassification
from domain.entities.lm_codes import LMCode
from typing import List

class ISmellRepository(ABC):
    @abstractmethod
    def save_all(self, smells: SmellOccurrence):
        pass

    @abstractmethod
    def get_ast_codes_by_id(self, id: str) -> List[SmellOccurrence]:
        pass

    @abstractmethod
    def get_lm_codes_by_id(self, id: str) -> List[LMCode]:
        pass
    
    @abstractmethod
    def get_ml_codes_by_id(self, id: str) -> List[MLClassification]:
        pass

    @abstractmethod
    def get_dl_codes_by_id(self, id: str) -> List[DLClassification]:
        pass
