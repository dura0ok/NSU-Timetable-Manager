from dataclasses import dataclass


@dataclass(frozen=True)
class SubjectName:
    full_name: str
    short_name: str
