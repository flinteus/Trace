from enum import StrEnum, auto

class StatusType(StrEnum):
    ONLINE = auto()
    OFFLINE = auto()
    ERROR = auto()

class MessageType(StrEnum):
    LINE = auto()
    ERROR = auto()
    EOF = auto()
    
