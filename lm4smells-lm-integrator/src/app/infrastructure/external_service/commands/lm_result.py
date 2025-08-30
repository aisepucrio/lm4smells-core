from pydantic import BaseModel

class LMResult(BaseModel):
    smell_type: str
    explanation: str
