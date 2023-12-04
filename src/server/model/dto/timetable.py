from dataclasses import dataclass

from .cell import Cell
from .times import Times


@dataclass(frozen=True)
class Timetable:
    cells: list[Cell]  # Stored by lines
    times: Times
