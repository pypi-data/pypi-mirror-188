from google.protobuf import timestamp_pb2 as _timestamp_pb2
import ace_pb2 as _ace_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class addworkitemqueue(_message.Message):
    __slots__ = ["_acl", "amqpqueue", "failed_wiq", "failed_wiqid", "initialdelay", "maxretries", "name", "projectid", "retrydelay", "robotqueue", "skiprole", "success_wiq", "success_wiqid"]
    AMQPQUEUE_FIELD_NUMBER: _ClassVar[int]
    FAILED_WIQID_FIELD_NUMBER: _ClassVar[int]
    FAILED_WIQ_FIELD_NUMBER: _ClassVar[int]
    INITIALDELAY_FIELD_NUMBER: _ClassVar[int]
    MAXRETRIES_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    PROJECTID_FIELD_NUMBER: _ClassVar[int]
    RETRYDELAY_FIELD_NUMBER: _ClassVar[int]
    ROBOTQUEUE_FIELD_NUMBER: _ClassVar[int]
    SKIPROLE_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_WIQID_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_WIQ_FIELD_NUMBER: _ClassVar[int]
    _ACL_FIELD_NUMBER: _ClassVar[int]
    _acl: _containers.RepeatedCompositeFieldContainer[_ace_pb2.ace]
    amqpqueue: str
    failed_wiq: str
    failed_wiqid: str
    initialdelay: int
    maxretries: int
    name: str
    projectid: str
    retrydelay: int
    robotqueue: str
    skiprole: bool
    success_wiq: str
    success_wiqid: str
    def __init__(self, name: _Optional[str] = ..., robotqueue: _Optional[str] = ..., amqpqueue: _Optional[str] = ..., projectid: _Optional[str] = ..., skiprole: bool = ..., maxretries: _Optional[int] = ..., initialdelay: _Optional[int] = ..., retrydelay: _Optional[int] = ..., success_wiqid: _Optional[str] = ..., failed_wiqid: _Optional[str] = ..., success_wiq: _Optional[str] = ..., failed_wiq: _Optional[str] = ..., _acl: _Optional[_Iterable[_Union[_ace_pb2.ace, _Mapping]]] = ...) -> None: ...

class addworkitemqueuereply(_message.Message):
    __slots__ = ["workitemqueue"]
    WORKITEMQUEUE_FIELD_NUMBER: _ClassVar[int]
    workitemqueue: workitemqueue
    def __init__(self, workitemqueue: _Optional[_Union[workitemqueue, _Mapping]] = ...) -> None: ...

class deleteworkitem(_message.Message):
    __slots__ = ["_id"]
    _ID_FIELD_NUMBER: _ClassVar[int]
    _id: str
    def __init__(self, _id: _Optional[str] = ...) -> None: ...

class deleteworkitemreply(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class popworkitem(_message.Message):
    __slots__ = ["compressed", "includefiles", "wiq", "wiqid"]
    COMPRESSED_FIELD_NUMBER: _ClassVar[int]
    INCLUDEFILES_FIELD_NUMBER: _ClassVar[int]
    WIQID_FIELD_NUMBER: _ClassVar[int]
    WIQ_FIELD_NUMBER: _ClassVar[int]
    compressed: bool
    includefiles: bool
    wiq: str
    wiqid: str
    def __init__(self, wiq: _Optional[str] = ..., wiqid: _Optional[str] = ..., includefiles: bool = ..., compressed: bool = ...) -> None: ...

class popworkitemreply(_message.Message):
    __slots__ = ["workitem"]
    WORKITEM_FIELD_NUMBER: _ClassVar[int]
    workitem: workitem
    def __init__(self, workitem: _Optional[_Union[workitem, _Mapping]] = ...) -> None: ...

class pushworkitem(_message.Message):
    __slots__ = ["failed_wiq", "failed_wiqid", "files", "name", "nextrun", "payload", "priority", "success_wiq", "success_wiqid", "wiq", "wiqid"]
    FAILED_WIQID_FIELD_NUMBER: _ClassVar[int]
    FAILED_WIQ_FIELD_NUMBER: _ClassVar[int]
    FILES_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    NEXTRUN_FIELD_NUMBER: _ClassVar[int]
    PAYLOAD_FIELD_NUMBER: _ClassVar[int]
    PRIORITY_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_WIQID_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_WIQ_FIELD_NUMBER: _ClassVar[int]
    WIQID_FIELD_NUMBER: _ClassVar[int]
    WIQ_FIELD_NUMBER: _ClassVar[int]
    failed_wiq: str
    failed_wiqid: str
    files: _containers.RepeatedCompositeFieldContainer[workitemfile]
    name: str
    nextrun: _timestamp_pb2.Timestamp
    payload: str
    priority: int
    success_wiq: str
    success_wiqid: str
    wiq: str
    wiqid: str
    def __init__(self, wiq: _Optional[str] = ..., wiqid: _Optional[str] = ..., name: _Optional[str] = ..., payload: _Optional[str] = ..., nextrun: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., success_wiqid: _Optional[str] = ..., failed_wiqid: _Optional[str] = ..., success_wiq: _Optional[str] = ..., failed_wiq: _Optional[str] = ..., priority: _Optional[int] = ..., files: _Optional[_Iterable[_Union[workitemfile, _Mapping]]] = ...) -> None: ...

class pushworkitemreply(_message.Message):
    __slots__ = ["workitem"]
    WORKITEM_FIELD_NUMBER: _ClassVar[int]
    workitem: workitem
    def __init__(self, workitem: _Optional[_Union[workitem, _Mapping]] = ...) -> None: ...

class pushworkitems(_message.Message):
    __slots__ = ["failed_wiq", "failed_wiqid", "items", "nextrun", "priority", "success_wiq", "success_wiqid", "wiq", "wiqid"]
    FAILED_WIQID_FIELD_NUMBER: _ClassVar[int]
    FAILED_WIQ_FIELD_NUMBER: _ClassVar[int]
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    NEXTRUN_FIELD_NUMBER: _ClassVar[int]
    PRIORITY_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_WIQID_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_WIQ_FIELD_NUMBER: _ClassVar[int]
    WIQID_FIELD_NUMBER: _ClassVar[int]
    WIQ_FIELD_NUMBER: _ClassVar[int]
    failed_wiq: str
    failed_wiqid: str
    items: _containers.RepeatedCompositeFieldContainer[workitem]
    nextrun: _timestamp_pb2.Timestamp
    priority: int
    success_wiq: str
    success_wiqid: str
    wiq: str
    wiqid: str
    def __init__(self, wiq: _Optional[str] = ..., wiqid: _Optional[str] = ..., nextrun: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., success_wiqid: _Optional[str] = ..., failed_wiqid: _Optional[str] = ..., success_wiq: _Optional[str] = ..., failed_wiq: _Optional[str] = ..., priority: _Optional[int] = ..., items: _Optional[_Iterable[_Union[workitem, _Mapping]]] = ...) -> None: ...

class pushworkitemsreply(_message.Message):
    __slots__ = ["workitems"]
    WORKITEMS_FIELD_NUMBER: _ClassVar[int]
    workitems: _containers.RepeatedCompositeFieldContainer[workitem]
    def __init__(self, workitems: _Optional[_Iterable[_Union[workitem, _Mapping]]] = ...) -> None: ...

class updateworkitem(_message.Message):
    __slots__ = ["ignoremaxretries", "workitem"]
    IGNOREMAXRETRIES_FIELD_NUMBER: _ClassVar[int]
    WORKITEM_FIELD_NUMBER: _ClassVar[int]
    ignoremaxretries: bool
    workitem: workitem
    def __init__(self, workitem: _Optional[_Union[workitem, _Mapping]] = ..., ignoremaxretries: bool = ...) -> None: ...

class updateworkitemreply(_message.Message):
    __slots__ = ["workitem"]
    WORKITEM_FIELD_NUMBER: _ClassVar[int]
    workitem: workitem
    def __init__(self, workitem: _Optional[_Union[workitem, _Mapping]] = ...) -> None: ...

class workitem(_message.Message):
    __slots__ = ["_id", "errormessage", "errorsource", "errortype", "failed_wiq", "failed_wiqid", "files", "lastrun", "name", "nextrun", "payload", "priority", "retries", "state", "success_wiq", "success_wiqid", "username", "wiq", "wiqid"]
    ERRORMESSAGE_FIELD_NUMBER: _ClassVar[int]
    ERRORSOURCE_FIELD_NUMBER: _ClassVar[int]
    ERRORTYPE_FIELD_NUMBER: _ClassVar[int]
    FAILED_WIQID_FIELD_NUMBER: _ClassVar[int]
    FAILED_WIQ_FIELD_NUMBER: _ClassVar[int]
    FILES_FIELD_NUMBER: _ClassVar[int]
    LASTRUN_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    NEXTRUN_FIELD_NUMBER: _ClassVar[int]
    PAYLOAD_FIELD_NUMBER: _ClassVar[int]
    PRIORITY_FIELD_NUMBER: _ClassVar[int]
    RETRIES_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_WIQID_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_WIQ_FIELD_NUMBER: _ClassVar[int]
    USERNAME_FIELD_NUMBER: _ClassVar[int]
    WIQID_FIELD_NUMBER: _ClassVar[int]
    WIQ_FIELD_NUMBER: _ClassVar[int]
    _ID_FIELD_NUMBER: _ClassVar[int]
    _id: str
    errormessage: str
    errorsource: str
    errortype: str
    failed_wiq: str
    failed_wiqid: str
    files: _containers.RepeatedCompositeFieldContainer[workitemfile]
    lastrun: _timestamp_pb2.Timestamp
    name: str
    nextrun: _timestamp_pb2.Timestamp
    payload: str
    priority: int
    retries: int
    state: str
    success_wiq: str
    success_wiqid: str
    username: str
    wiq: str
    wiqid: str
    def __init__(self, _id: _Optional[str] = ..., name: _Optional[str] = ..., payload: _Optional[str] = ..., priority: _Optional[int] = ..., nextrun: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., lastrun: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., files: _Optional[_Iterable[_Union[workitemfile, _Mapping]]] = ..., state: _Optional[str] = ..., wiq: _Optional[str] = ..., wiqid: _Optional[str] = ..., retries: _Optional[int] = ..., username: _Optional[str] = ..., success_wiqid: _Optional[str] = ..., failed_wiqid: _Optional[str] = ..., success_wiq: _Optional[str] = ..., failed_wiq: _Optional[str] = ..., errormessage: _Optional[str] = ..., errorsource: _Optional[str] = ..., errortype: _Optional[str] = ...) -> None: ...

class workitemfile(_message.Message):
    __slots__ = ["_id", "compressed", "file", "filename"]
    COMPRESSED_FIELD_NUMBER: _ClassVar[int]
    FILENAME_FIELD_NUMBER: _ClassVar[int]
    FILE_FIELD_NUMBER: _ClassVar[int]
    _ID_FIELD_NUMBER: _ClassVar[int]
    _id: str
    compressed: bool
    file: bytes
    filename: str
    def __init__(self, filename: _Optional[str] = ..., _id: _Optional[str] = ..., compressed: bool = ..., file: _Optional[bytes] = ...) -> None: ...

class workitemqueue(_message.Message):
    __slots__ = ["_acl", "_created", "_createdby", "_createdbyid", "_id", "_modified", "_modifiedby", "_modifiedbyid", "_version", "amqpqueue", "failed_wiq", "failed_wiqid", "initialdelay", "maxretries", "name", "projectid", "retrydelay", "robotqueue", "success_wiq", "success_wiqid", "usersrole", "workflowid"]
    AMQPQUEUE_FIELD_NUMBER: _ClassVar[int]
    FAILED_WIQID_FIELD_NUMBER: _ClassVar[int]
    FAILED_WIQ_FIELD_NUMBER: _ClassVar[int]
    INITIALDELAY_FIELD_NUMBER: _ClassVar[int]
    MAXRETRIES_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    PROJECTID_FIELD_NUMBER: _ClassVar[int]
    RETRYDELAY_FIELD_NUMBER: _ClassVar[int]
    ROBOTQUEUE_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_WIQID_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_WIQ_FIELD_NUMBER: _ClassVar[int]
    USERSROLE_FIELD_NUMBER: _ClassVar[int]
    WORKFLOWID_FIELD_NUMBER: _ClassVar[int]
    _ACL_FIELD_NUMBER: _ClassVar[int]
    _CREATEDBYID_FIELD_NUMBER: _ClassVar[int]
    _CREATEDBY_FIELD_NUMBER: _ClassVar[int]
    _CREATED_FIELD_NUMBER: _ClassVar[int]
    _ID_FIELD_NUMBER: _ClassVar[int]
    _MODIFIEDBYID_FIELD_NUMBER: _ClassVar[int]
    _MODIFIEDBY_FIELD_NUMBER: _ClassVar[int]
    _MODIFIED_FIELD_NUMBER: _ClassVar[int]
    _VERSION_FIELD_NUMBER: _ClassVar[int]
    _acl: _containers.RepeatedCompositeFieldContainer[_ace_pb2.ace]
    _created: _timestamp_pb2.Timestamp
    _createdby: str
    _createdbyid: str
    _id: str
    _modified: _timestamp_pb2.Timestamp
    _modifiedby: str
    _modifiedbyid: str
    _version: int
    amqpqueue: str
    failed_wiq: str
    failed_wiqid: str
    initialdelay: int
    maxretries: int
    name: str
    projectid: str
    retrydelay: int
    robotqueue: str
    success_wiq: str
    success_wiqid: str
    usersrole: str
    workflowid: str
    def __init__(self, workflowid: _Optional[str] = ..., robotqueue: _Optional[str] = ..., amqpqueue: _Optional[str] = ..., projectid: _Optional[str] = ..., usersrole: _Optional[str] = ..., maxretries: _Optional[int] = ..., retrydelay: _Optional[int] = ..., initialdelay: _Optional[int] = ..., success_wiqid: _Optional[str] = ..., failed_wiqid: _Optional[str] = ..., success_wiq: _Optional[str] = ..., failed_wiq: _Optional[str] = ..., _id: _Optional[str] = ..., _acl: _Optional[_Iterable[_Union[_ace_pb2.ace, _Mapping]]] = ..., name: _Optional[str] = ..., _createdbyid: _Optional[str] = ..., _createdby: _Optional[str] = ..., _created: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., _modifiedbyid: _Optional[str] = ..., _modifiedby: _Optional[str] = ..., _modified: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., _version: _Optional[int] = ...) -> None: ...
