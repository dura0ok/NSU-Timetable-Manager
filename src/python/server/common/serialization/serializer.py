from abc import ABC, abstractmethod

from ..json_serializable import JSONSerializable


class Serializer(ABC):
    @abstractmethod
    def serialize(self, serializable: JSONSerializable) -> bytes:
        pass
