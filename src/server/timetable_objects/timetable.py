from dataclasses import dataclass
from typing import List

from .cell import Cell
from json_serializable import JSONSerializable


@dataclass
class Timetable(JSONSerializable):
    cells: List[Cell]  # Stored by lines
    times: List[str]


def create_empty_timetable(times: List[str]) -> Timetable:
    return Timetable(cells=[], times=times)
