from pydantic import BaseModel, Field
from typing import Optional, List, Literal
from datetime import datetime
from app.models.enum import MessageType

class LogFile(BaseModel):
    name: str
    path: str
    size: int
    modified: datetime
    readable: bool = True


class LogQueryParams(BaseModel):

    lines: Optional[int] = Field(
        default=100,
        ge=1,
        le=10000,
        description="Количество строк для чтения (от 1 до 10000)"
    )
    offset: Optional[int] = Field(
        default=0,
        ge=0,
        description="Смещение от начала файла в байтах (для пагинации)"
    )
    search: Optional[str] = Field(
        default=None,
        description="Поиск по подстроке (опционально)"
    )
    since: Optional[datetime] = Field(
        default=None,
        description="Читать логи только после указанной даты"
    )

class LogEntry(BaseModel):

    line_number: int     
    content: str       
    timestamp: Optional[datetime] = None  
    level: Optional[str] = None
    
class LogResponse(BaseModel):

    log_name: str           
    total_lines: int        
    returned_lines: int     
    entries: List[LogEntry] 
    has_more: bool          
    next_offset: Optional[int] = None

class LogTailResponse(BaseModel):
    log_name: str
    lines: List[str]    
    total_lines: int


class LogStreamMessage(BaseModel):
        
    type: Literal[MessageType.LINE, MessageType.ERROR, MessageType.EOF]  
    data: str                              
    line_number: Optional[int] = None

class LogSearchResult(BaseModel):

    query: str          # что искали
    matches: int        # количество совпадений
    results: List[LogEntry]

