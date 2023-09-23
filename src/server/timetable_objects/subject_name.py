from dataclasses import dataclass
from typing import Optional

import dataclass_wizard


@dataclass(frozen=True)
class SubjectName(dataclass_wizard.JSONWizard):
    full_name: Optional[str]
    short_name: Optional[str]
    is_empty: bool = False


def empty_subject_name() -> SubjectName:
    return SubjectName(full_name=None, short_name=None, is_empty=True)
