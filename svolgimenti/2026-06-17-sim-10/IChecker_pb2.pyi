from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class Temperature(_message.Message):
    __slots__ = ("temperature",)
    TEMPERATURE_FIELD_NUMBER: _ClassVar[int]
    temperature: int
    def __init__(self, temperature: _Optional[int] = ...) -> None: ...

class Ack(_message.Message):
    __slots__ = ("status",)
    STATUS_FIELD_NUMBER: _ClassVar[int]
    status: str
    def __init__(self, status: _Optional[str] = ...) -> None: ...

class Empty(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class Average(_message.Message):
    __slots__ = ("avg",)
    AVG_FIELD_NUMBER: _ClassVar[int]
    avg: float
    def __init__(self, avg: _Optional[float] = ...) -> None: ...
