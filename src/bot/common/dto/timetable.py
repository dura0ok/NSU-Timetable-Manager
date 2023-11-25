from dataclasses import dataclass
from typing import List

from dataclasses_json import dataclass_json

from .cell import Cell
from .times import Times


@dataclass_json
@dataclass
class Timetable:
    cells: List[Cell]  # Stored by lines
    times: Times
