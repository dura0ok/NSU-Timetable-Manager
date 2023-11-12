from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class Times:
    times: List[str]
