from dataclasses import dataclass
from typing import Optional

import dataclass_wizard

from .room_location import RoomLocation


@dataclass(frozen=True)
class Room(dataclass_wizard.JSONWizard):
    name: Optional[str]
    location: Optional[RoomLocation]
    is_empty: bool = False


def empty_room() -> Room:
    return Room(name=None, location=None, is_empty=True)
