from dataclasses import dataclass
from typing import Optional

import dataclass_wizard


@dataclass(frozen=True)
class RoomLocation(dataclass_wizard.JSONWizard):
    block: Optional[str]
    level: Optional[int]
    x: Optional[int]
    y: Optional[int]
    is_empty: bool = False


def empty_room_location() -> RoomLocation:
    return RoomLocation(block=None, level=None, x=None, y=None, is_empty=True)
