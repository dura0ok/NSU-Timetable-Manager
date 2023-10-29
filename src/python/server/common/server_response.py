from dataclasses import dataclass
from typing import Optional

from common import ServerCodes
from .json_serializable import JSONSerializable


@dataclass(frozen=True)
class ServerResponse(JSONSerializable):
    result: Optional[JSONSerializable]
    is_success: bool = True
    message: str = 'Success'
    code: ServerCodes = ServerCodes.SUCCESS


def create_error_parsing_result(message: str, code: ServerCodes) -> ServerResponse:
    return ServerResponse(result=None, is_success=False, message=message, code=code)
