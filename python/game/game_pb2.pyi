from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class NewGameRequest(_message.Message):
    __slots__ = ("size_x", "size_y", "p")
    SIZE_X_FIELD_NUMBER: _ClassVar[int]
    SIZE_Y_FIELD_NUMBER: _ClassVar[int]
    P_FIELD_NUMBER: _ClassVar[int]
    size_x: int
    size_y: int
    p: float
    def __init__(self, size_x: _Optional[int] = ..., size_y: _Optional[int] = ..., p: _Optional[float] = ...) -> None: ...

class NewGameReply(_message.Message):
    __slots__ = ("data",)
    DATA_FIELD_NUMBER: _ClassVar[int]
    data: str
    def __init__(self, data: _Optional[str] = ...) -> None: ...

class HelloRequest(_message.Message):
    __slots__ = ("name",)
    NAME_FIELD_NUMBER: _ClassVar[int]
    name: str
    def __init__(self, name: _Optional[str] = ...) -> None: ...

class HelloReply(_message.Message):
    __slots__ = ("message",)
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    message: str
    def __init__(self, message: _Optional[str] = ...) -> None: ...

class ShowAllSessionsRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class SessionDetailsReply(_message.Message):
    __slots__ = ("session_id", "date", "metadata", "steps", "last")
    SESSION_ID_FIELD_NUMBER: _ClassVar[int]
    DATE_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    STEPS_FIELD_NUMBER: _ClassVar[int]
    LAST_FIELD_NUMBER: _ClassVar[int]
    session_id: str
    date: str
    metadata: str
    steps: int
    last: str
    def __init__(self, session_id: _Optional[str] = ..., date: _Optional[str] = ..., metadata: _Optional[str] = ..., steps: _Optional[int] = ..., last: _Optional[str] = ...) -> None: ...

class GetCurrentSessionRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class SetCurrentSessionRequest(_message.Message):
    __slots__ = ("session_id",)
    SESSION_ID_FIELD_NUMBER: _ClassVar[int]
    session_id: str
    def __init__(self, session_id: _Optional[str] = ...) -> None: ...

class GetStateRequest(_message.Message):
    __slots__ = ("step",)
    STEP_FIELD_NUMBER: _ClassVar[int]
    step: int
    def __init__(self, step: _Optional[int] = ...) -> None: ...

class GetStateReply(_message.Message):
    __slots__ = ("data",)
    DATA_FIELD_NUMBER: _ClassVar[int]
    data: str
    def __init__(self, data: _Optional[str] = ...) -> None: ...

class StepRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class StepReply(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...
