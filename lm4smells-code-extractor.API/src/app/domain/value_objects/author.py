from dataclasses import dataclass
from enum import Enum

@dataclass(frozen=True)
class Author(Enum):
    dpy = "Dpy"