from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class queueevent(_message.Message):
    __slots__ = ["correlationId", "data", "exchangename", "queuename", "replyto", "routingkey"]
    CORRELATIONID_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    EXCHANGENAME_FIELD_NUMBER: _ClassVar[int]
    QUEUENAME_FIELD_NUMBER: _ClassVar[int]
    REPLYTO_FIELD_NUMBER: _ClassVar[int]
    ROUTINGKEY_FIELD_NUMBER: _ClassVar[int]
    correlationId: str
    data: str
    exchangename: str
    queuename: str
    replyto: str
    routingkey: str
    def __init__(self, queuename: _Optional[str] = ..., correlationId: _Optional[str] = ..., replyto: _Optional[str] = ..., routingkey: _Optional[str] = ..., exchangename: _Optional[str] = ..., data: _Optional[str] = ...) -> None: ...

class queuemessage(_message.Message):
    __slots__ = ["correlationId", "data", "exchangename", "queuename", "replyto", "routingkey", "striptoken"]
    CORRELATIONID_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    EXCHANGENAME_FIELD_NUMBER: _ClassVar[int]
    QUEUENAME_FIELD_NUMBER: _ClassVar[int]
    REPLYTO_FIELD_NUMBER: _ClassVar[int]
    ROUTINGKEY_FIELD_NUMBER: _ClassVar[int]
    STRIPTOKEN_FIELD_NUMBER: _ClassVar[int]
    correlationId: str
    data: str
    exchangename: str
    queuename: str
    replyto: str
    routingkey: str
    striptoken: bool
    def __init__(self, queuename: _Optional[str] = ..., correlationId: _Optional[str] = ..., replyto: _Optional[str] = ..., routingkey: _Optional[str] = ..., exchangename: _Optional[str] = ..., data: _Optional[str] = ..., striptoken: bool = ...) -> None: ...

class queuemessagereply(_message.Message):
    __slots__ = ["correlationId", "data", "exchangename", "queuename", "replyto", "routingkey"]
    CORRELATIONID_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    EXCHANGENAME_FIELD_NUMBER: _ClassVar[int]
    QUEUENAME_FIELD_NUMBER: _ClassVar[int]
    REPLYTO_FIELD_NUMBER: _ClassVar[int]
    ROUTINGKEY_FIELD_NUMBER: _ClassVar[int]
    correlationId: str
    data: str
    exchangename: str
    queuename: str
    replyto: str
    routingkey: str
    def __init__(self, queuename: _Optional[str] = ..., correlationId: _Optional[str] = ..., replyto: _Optional[str] = ..., routingkey: _Optional[str] = ..., exchangename: _Optional[str] = ..., data: _Optional[str] = ...) -> None: ...

class registerexchange(_message.Message):
    __slots__ = ["addqueue", "algorithm", "exchangename", "routingkey"]
    ADDQUEUE_FIELD_NUMBER: _ClassVar[int]
    ALGORITHM_FIELD_NUMBER: _ClassVar[int]
    EXCHANGENAME_FIELD_NUMBER: _ClassVar[int]
    ROUTINGKEY_FIELD_NUMBER: _ClassVar[int]
    addqueue: bool
    algorithm: str
    exchangename: str
    routingkey: str
    def __init__(self, exchangename: _Optional[str] = ..., algorithm: _Optional[str] = ..., routingkey: _Optional[str] = ..., addqueue: bool = ...) -> None: ...

class registerexchangereply(_message.Message):
    __slots__ = ["queuename"]
    QUEUENAME_FIELD_NUMBER: _ClassVar[int]
    queuename: str
    def __init__(self, queuename: _Optional[str] = ...) -> None: ...

class registerqueue(_message.Message):
    __slots__ = ["queuename"]
    QUEUENAME_FIELD_NUMBER: _ClassVar[int]
    queuename: str
    def __init__(self, queuename: _Optional[str] = ...) -> None: ...

class registerqueuereply(_message.Message):
    __slots__ = ["queuename"]
    QUEUENAME_FIELD_NUMBER: _ClassVar[int]
    queuename: str
    def __init__(self, queuename: _Optional[str] = ...) -> None: ...

class unregisterqueue(_message.Message):
    __slots__ = ["queuename"]
    QUEUENAME_FIELD_NUMBER: _ClassVar[int]
    queuename: str
    def __init__(self, queuename: _Optional[str] = ...) -> None: ...

class unregisterqueuereply(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...
