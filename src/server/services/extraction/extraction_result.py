from dataclasses import dataclass
from typing import Optional

from .extraction_codes import ExtractionCodes


@dataclass(frozen=True)
class ExtractionResult:
    result: Optional[object]
    is_success: bool = True
    message: str = 'Success'
    code: ExtractionCodes = ExtractionCodes.SUCCESS


def create_error_extraction_result(message: str, code: ExtractionCodes) -> ExtractionResult:
    return ExtractionResult(result=None, is_success=False, message=message, code=code)
