from dataclasses import dataclass
from typing import List

from serialization import JSONSerializable


@dataclass(frozen=True)
class Times(JSONSerializable):
    times: List[str]
