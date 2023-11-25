from dataclasses import dataclass
from typing import Optional

from dataclasses_json import dataclass_json

from .server_codes import ServerCodes


@dataclass_json
@dataclass(frozen=True)
class ServerResponse:
    result: Optional[object]
    is_success: bool = True
    message: str = 'Success'
    code: ServerCodes = ServerCodes.SUCCESS


def create_error_server_response(message: str, code: ServerCodes) -> ServerResponse:
    return ServerResponse(result=None, is_success=False, message=message, code=code)
