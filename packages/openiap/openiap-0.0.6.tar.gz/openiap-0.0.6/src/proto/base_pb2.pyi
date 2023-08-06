from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf import any_pb2 as _any_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class beginstream(_message.Message):
    __slots__ = ["checksum", "stat"]
    CHECKSUM_FIELD_NUMBER: _ClassVar[int]
    STAT_FIELD_NUMBER: _ClassVar[int]
    checksum: str
    stat: stat
    def __init__(self, checksum: _Optional[str] = ..., stat: _Optional[_Union[stat, _Mapping]] = ...) -> None: ...

class clientconsole(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class console(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class customcommand(_message.Message):
    __slots__ = ["command", "data", "id", "name"]
    COMMAND_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    command: str
    data: str
    id: str
    name: str
    def __init__(self, command: _Optional[str] = ..., id: _Optional[str] = ..., name: _Optional[str] = ..., data: _Optional[str] = ...) -> None: ...

class customcommandreply(_message.Message):
    __slots__ = ["result"]
    RESULT_FIELD_NUMBER: _ClassVar[int]
    result: str
    def __init__(self, result: _Optional[str] = ...) -> None: ...

class download(_message.Message):
    __slots__ = ["filename", "id"]
    FILENAME_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    filename: str
    id: str
    def __init__(self, id: _Optional[str] = ..., filename: _Optional[str] = ...) -> None: ...

class downloadreply(_message.Message):
    __slots__ = ["filename", "id", "mimetype"]
    FILENAME_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    MIMETYPE_FIELD_NUMBER: _ClassVar[int]
    filename: str
    id: str
    mimetype: str
    def __init__(self, id: _Optional[str] = ..., filename: _Optional[str] = ..., mimetype: _Optional[str] = ...) -> None: ...

class endstream(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class envelope(_message.Message):
    __slots__ = ["command", "data", "hash", "id", "priority", "rid", "seq", "spanid", "traceid"]
    COMMAND_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    HASH_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    PRIORITY_FIELD_NUMBER: _ClassVar[int]
    RID_FIELD_NUMBER: _ClassVar[int]
    SEQ_FIELD_NUMBER: _ClassVar[int]
    SPANID_FIELD_NUMBER: _ClassVar[int]
    TRACEID_FIELD_NUMBER: _ClassVar[int]
    command: str
    data: _any_pb2.Any
    hash: str
    id: str
    priority: int
    rid: str
    seq: int
    spanid: str
    traceid: str
    def __init__(self, command: _Optional[str] = ..., priority: _Optional[int] = ..., seq: _Optional[int] = ..., hash: _Optional[str] = ..., id: _Optional[str] = ..., rid: _Optional[str] = ..., traceid: _Optional[str] = ..., spanid: _Optional[str] = ..., data: _Optional[_Union[_any_pb2.Any, _Mapping]] = ...) -> None: ...

class error(_message.Message):
    __slots__ = ["code", "message", "stack"]
    CODE_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    STACK_FIELD_NUMBER: _ClassVar[int]
    code: int
    message: str
    stack: str
    def __init__(self, message: _Optional[str] = ..., code: _Optional[int] = ..., stack: _Optional[str] = ...) -> None: ...

class getelement(_message.Message):
    __slots__ = ["xpath"]
    XPATH_FIELD_NUMBER: _ClassVar[int]
    xpath: str
    def __init__(self, xpath: _Optional[str] = ...) -> None: ...

class noop(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class ping(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class pong(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class refreshtoken(_message.Message):
    __slots__ = ["jwt", "user", "username"]
    JWT_FIELD_NUMBER: _ClassVar[int]
    USERNAME_FIELD_NUMBER: _ClassVar[int]
    USER_FIELD_NUMBER: _ClassVar[int]
    jwt: str
    user: user
    username: str
    def __init__(self, username: _Optional[str] = ..., jwt: _Optional[str] = ..., user: _Optional[_Union[user, _Mapping]] = ...) -> None: ...

class role(_message.Message):
    __slots__ = ["_id", "name"]
    NAME_FIELD_NUMBER: _ClassVar[int]
    _ID_FIELD_NUMBER: _ClassVar[int]
    _id: str
    name: str
    def __init__(self, _id: _Optional[str] = ..., name: _Optional[str] = ...) -> None: ...

class send(_message.Message):
    __slots__ = ["count"]
    COUNT_FIELD_NUMBER: _ClassVar[int]
    count: int
    def __init__(self, count: _Optional[int] = ...) -> None: ...

class signin(_message.Message):
    __slots__ = ["jwt", "password", "ping", "username"]
    JWT_FIELD_NUMBER: _ClassVar[int]
    PASSWORD_FIELD_NUMBER: _ClassVar[int]
    PING_FIELD_NUMBER: _ClassVar[int]
    USERNAME_FIELD_NUMBER: _ClassVar[int]
    jwt: str
    password: str
    ping: bool
    username: str
    def __init__(self, username: _Optional[str] = ..., password: _Optional[str] = ..., jwt: _Optional[str] = ..., ping: bool = ...) -> None: ...

class signinreply(_message.Message):
    __slots__ = ["jwt", "user"]
    JWT_FIELD_NUMBER: _ClassVar[int]
    USER_FIELD_NUMBER: _ClassVar[int]
    jwt: str
    user: user
    def __init__(self, jwt: _Optional[str] = ..., user: _Optional[_Union[user, _Mapping]] = ...) -> None: ...

class stat(_message.Message):
    __slots__ = ["birthtimeMs", "blksize", "blocks", "ctime", "ctimeMs", "dev", "gid", "ino", "mode", "mtime", "mtimeMs", "nlink", "rdev", "size", "uid"]
    BIRTHTIMEMS_FIELD_NUMBER: _ClassVar[int]
    BLKSIZE_FIELD_NUMBER: _ClassVar[int]
    BLOCKS_FIELD_NUMBER: _ClassVar[int]
    CTIMEMS_FIELD_NUMBER: _ClassVar[int]
    CTIME_FIELD_NUMBER: _ClassVar[int]
    DEV_FIELD_NUMBER: _ClassVar[int]
    GID_FIELD_NUMBER: _ClassVar[int]
    INO_FIELD_NUMBER: _ClassVar[int]
    MODE_FIELD_NUMBER: _ClassVar[int]
    MTIMEMS_FIELD_NUMBER: _ClassVar[int]
    MTIME_FIELD_NUMBER: _ClassVar[int]
    NLINK_FIELD_NUMBER: _ClassVar[int]
    RDEV_FIELD_NUMBER: _ClassVar[int]
    SIZE_FIELD_NUMBER: _ClassVar[int]
    UID_FIELD_NUMBER: _ClassVar[int]
    birthtimeMs: float
    blksize: int
    blocks: int
    ctime: _timestamp_pb2.Timestamp
    ctimeMs: float
    dev: int
    gid: int
    ino: int
    mode: int
    mtime: _timestamp_pb2.Timestamp
    mtimeMs: float
    nlink: int
    rdev: int
    size: int
    uid: int
    def __init__(self, birthtimeMs: _Optional[float] = ..., blksize: _Optional[int] = ..., blocks: _Optional[int] = ..., ctime: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., ctimeMs: _Optional[float] = ..., dev: _Optional[int] = ..., gid: _Optional[int] = ..., ino: _Optional[int] = ..., mode: _Optional[int] = ..., mtime: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., mtimeMs: _Optional[float] = ..., nlink: _Optional[int] = ..., rdev: _Optional[int] = ..., size: _Optional[int] = ..., uid: _Optional[int] = ...) -> None: ...

class stream(_message.Message):
    __slots__ = ["data"]
    DATA_FIELD_NUMBER: _ClassVar[int]
    data: bytes
    def __init__(self, data: _Optional[bytes] = ...) -> None: ...

class upload(_message.Message):
    __slots__ = ["filename", "mimetype"]
    FILENAME_FIELD_NUMBER: _ClassVar[int]
    MIMETYPE_FIELD_NUMBER: _ClassVar[int]
    filename: str
    mimetype: str
    def __init__(self, filename: _Optional[str] = ..., mimetype: _Optional[str] = ...) -> None: ...

class uploadreply(_message.Message):
    __slots__ = ["bytes", "chunks", "elapsedTime", "filename", "id", "mb", "mbps"]
    BYTES_FIELD_NUMBER: _ClassVar[int]
    CHUNKS_FIELD_NUMBER: _ClassVar[int]
    ELAPSEDTIME_FIELD_NUMBER: _ClassVar[int]
    FILENAME_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    MBPS_FIELD_NUMBER: _ClassVar[int]
    MB_FIELD_NUMBER: _ClassVar[int]
    bytes: int
    chunks: int
    elapsedTime: int
    filename: str
    id: str
    mb: float
    mbps: float
    def __init__(self, id: _Optional[str] = ..., filename: _Optional[str] = ..., bytes: _Optional[int] = ..., chunks: _Optional[int] = ..., mb: _Optional[float] = ..., elapsedTime: _Optional[int] = ..., mbps: _Optional[float] = ...) -> None: ...

class user(_message.Message):
    __slots__ = ["_id", "email", "name", "roles", "username"]
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    ROLES_FIELD_NUMBER: _ClassVar[int]
    USERNAME_FIELD_NUMBER: _ClassVar[int]
    _ID_FIELD_NUMBER: _ClassVar[int]
    _id: str
    email: str
    name: str
    roles: _containers.RepeatedCompositeFieldContainer[role]
    username: str
    def __init__(self, _id: _Optional[str] = ..., name: _Optional[str] = ..., username: _Optional[str] = ..., email: _Optional[str] = ..., roles: _Optional[_Iterable[_Union[role, _Mapping]]] = ...) -> None: ...
