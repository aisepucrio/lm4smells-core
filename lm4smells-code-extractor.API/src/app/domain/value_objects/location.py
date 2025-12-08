from dataclasses import dataclass

@dataclass(frozen=True)
class Location:
    file_name: str
    start_line: int
    end_line: int