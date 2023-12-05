from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class Tutor:
    name: Optional[str]
    href: Optional[str]
    is_empty: bool = False


def create_empty_tutor() -> Tutor:
    return Tutor(name=None, href=None, is_empty=True)
