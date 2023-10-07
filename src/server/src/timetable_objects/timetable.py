from dataclasses import dataclass
from typing import List

from .cell import Cell
from src.serialization.serializable import Serializable


@dataclass
class Timetable(Serializable):
    cells: List[Cell]  # Stored by lines
    times: List[str]


def create_empty_timetable(times: List[str]) -> Timetable:
    return Timetable(cells=[], times=times)
