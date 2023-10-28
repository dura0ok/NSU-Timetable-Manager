from dataclasses import dataclass
from typing import List

from ..json_serializable import JSONSerializable


@dataclass(frozen=True)
class Times(JSONSerializable):
    times: List[str]
