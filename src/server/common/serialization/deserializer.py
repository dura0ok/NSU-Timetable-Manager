from abc import ABC, abstractmethod

from ..json_serializable import JSONSerializable


class Deserializer(ABC):
    @abstractmethod
    def deserialize(self, data: bytes) -> JSONSerializable:
        pass
