from dataclasses import dataclass
from typing import Optional

from .room_location import RoomLocation


@dataclass(frozen=True)
class Room:
    name: Optional[str]
    location: Optional[RoomLocation]
    is_empty: bool = False


def create_empty_room() -> Room:
    return Room(name=None, location=None, is_empty=True)
