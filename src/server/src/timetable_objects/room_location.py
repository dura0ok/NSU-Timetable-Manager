from dataclasses import dataclass
from typing import Optional

from src.serialization.serializable import Serializable


@dataclass(frozen=True)
class RoomLocation(Serializable):
    block: Optional[str]
    level: Optional[int]
    x: Optional[int]
    y: Optional[int]
    is_empty: bool = False


def create_empty_room_location() -> RoomLocation:
    return RoomLocation(block=None, level=None, x=None, y=None, is_empty=True)
