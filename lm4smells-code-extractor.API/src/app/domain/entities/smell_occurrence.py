from dataclasses import dataclass
from enum import Enum
from uuid import UUID, uuid4
from typing import Optional
from domain.value_objects.smell_type import SmellType
from domain.value_objects.location import Location
from domain.value_objects.metrics import Metrics
from datetime import datetime


@dataclass
class SmellOccurrence:
    id: UUID
    smell_type: SmellType
    description: str
    location: Location
    metrics: Metrics
    definition_author: str
    threshold_used: Optional[int] = None
    detected_at: Optional[str] = None
    created_at: Optional[datetime] = None