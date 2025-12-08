from dataclasses import dataclass
from uuid import UUID, uuid4
from typing import Optional, Dict, Any


@dataclass
class DLClassification:
    id: UUID
    file_name: str
    classification: str
    model_used: str
    element_name: Optional[str] = None
    element_type: Optional[str] = None
    confidence_score: Optional[float] = None
    metrics: Optional[Dict[str, Any]] = None
    raw_code: Optional[str] = None
    created_at: Optional[str] = None
