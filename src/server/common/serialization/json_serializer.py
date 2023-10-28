from .serializer import Serializer
from ..json_serializable import JSONSerializable


class JSONSerializer(Serializer):
    def serialize(self, serializable: JSONSerializable) -> bytes:
        return serializable.to_json().encode()
