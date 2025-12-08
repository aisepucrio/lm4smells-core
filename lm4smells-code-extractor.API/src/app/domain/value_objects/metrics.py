from dataclasses import dataclass
from typing import Optional

@dataclass(frozen=True)
class Metrics:
    PAR: Optional[int] = None      # Long Parameter List
    MLOC: Optional[int] = None     # Long Method
    WMC: Optional[int] = None      # Large Class
    NOA: Optional[int] = None 
    NOM: Optional[int] = None 
    LWMC:Optional[int] = None 
    LCOM:Optional[int] = None 
    DIT:Optional[int] = None 
    
