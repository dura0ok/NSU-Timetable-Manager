from dataclasses import dataclass
from typing import Optional

from serialization import JSONSerializable
from parsing_codes import ParsingCodes


@dataclass(frozen=True)
class ParsingResult(JSONSerializable):
    result: Optional[JSONSerializable]
    is_success: bool = True
    message: str = 'Success'
    code: ParsingCodes = ParsingCodes.SUCCESS


def create_error_parsing_result(message: str, code: ParsingCodes) -> ParsingResult:
    return ParsingResult(result=None, is_success=False, message=message, code=code)
