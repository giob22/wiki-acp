from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class Ping(_message.Message):
    __slots__ = ("latency",)
    LATENCY_FIELD_NUMBER: _ClassVar[int]
    latency: int
    def __init__(self, latency: _Optional[int] = ...) -> None: ...

class PingReply(_message.Message):
    __slots__ = ("pkt_rcvd",)
    PKT_RCVD_FIELD_NUMBER: _ClassVar[int]
    pkt_rcvd: int
    def __init__(self, pkt_rcvd: _Optional[int] = ...) -> None: ...

class Empty(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class Status(_message.Message):
    __slots__ = ("status",)
    STATUS_FIELD_NUMBER: _ClassVar[int]
    status: str
    def __init__(self, status: _Optional[str] = ...) -> None: ...
