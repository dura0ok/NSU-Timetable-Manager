from dataclasses import dataclass
from typing import List

import dataclass_wizard

from .cell import Cell


@dataclass
class Timetable(dataclass_wizard.JSONWizard):
    cells: List[Cell]  # Stored by lines
    weekdays: List[str]
    times: List[str]
