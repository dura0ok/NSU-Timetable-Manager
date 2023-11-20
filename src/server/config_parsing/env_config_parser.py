import os
from typing import Optional

from dotenv import load_dotenv

from .config_parser import ConfigParser


class EnvConfigParser(ConfigParser):
    __host_key_name: str = 'HOST'
    __port_key_name: str = 'PORT'

    def __init__(self) -> None:
        load_dotenv()

    def parse_host(self, def_value: str = '127.0.0.1') -> str:
        return os.getenv(EnvConfigParser.__host_key_name) or def_value

    def parse_port(self, def_value: int = 8000) -> int:
        port: Optional[str] = os.getenv(EnvConfigParser.__port_key_name)
        return int(port) if port is not None else def_value
