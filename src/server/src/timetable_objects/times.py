from dataclasses import dataclass
from typing import List

from src.serialization.serializable import Serializable


@dataclass(frozen=True)
class Times(Serializable):
    times: List[str]
