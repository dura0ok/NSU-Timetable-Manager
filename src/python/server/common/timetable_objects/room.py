from dataclasses import dataclass
from typing import Optional

from .room_location import RoomLocation
from ..json_serializable import JSONSerializable


@dataclass(frozen=True)
class Room(JSONSerializable):
    name: Optional[str]
    location: Optional[RoomLocation]
    is_empty: bool = False


def create_empty_room() -> Room:
    return Room(name=None, location=None, is_empty=True)
