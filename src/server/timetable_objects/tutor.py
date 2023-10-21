from dataclasses import dataclass
from typing import Optional

from serialization import JSONSerializable


@dataclass
class Tutor(JSONSerializable):
    name: Optional[str]
    href: Optional[str]
    is_empty: bool = False


def empty_tutor() -> Tutor:
    return Tutor(name=None, href=None, is_empty=True)
