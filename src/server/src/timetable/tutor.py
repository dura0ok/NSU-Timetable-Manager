from dataclasses import dataclass
from typing import Optional

import dataclass_wizard


@dataclass
class Tutor(dataclass_wizard.JSONWizard):
    name: Optional[str]
    href: Optional[str]
    is_empty: bool = False


def empty_tutor() -> Tutor:
    return Tutor(name=None, href=None, is_empty=True)
