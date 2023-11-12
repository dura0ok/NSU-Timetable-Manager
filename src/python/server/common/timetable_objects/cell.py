from dataclasses import dataclass
from typing import List

from .subject import Subject


@dataclass(frozen=True)
class Cell:
    subjects: List[Subject]
