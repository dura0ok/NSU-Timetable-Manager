from .deserializer import Deserializer
from ..json_serializable import JSONSerializable


class JSONDeserializer(Deserializer):
    def deserialize(self, data: bytes) -> JSONSerializable:
        return JSONSerializable.from_json(data.decode())
