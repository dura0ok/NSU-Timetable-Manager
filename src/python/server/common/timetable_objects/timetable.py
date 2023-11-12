from dataclasses import dataclass
from typing import List

from .cell import Cell
from .times import Times


@dataclass
class Timetable:
    cells: List[Cell]  # Stored by lines
    times: Times
