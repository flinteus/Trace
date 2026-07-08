from pydantic import BaseModel, Field
from typing import Optional, Literal
from datetime import datetime
from app.models.enum import StatusType

class AgentCreate(BaseModel):
    """схема для регистрации нового агента."""
    name: str = Field(..., description="Отображаемое имя сервера")
    hostname: str = Field(..., description="Хостнейм сервера (уникальный)")
    public_ip: Optional[str] = Field(None, description="Публичный IP")
    local_ip: Optional[str] = Field(None, description="Локальный IP")
    version: str = Field("1.0.0", description="Версия агента")

class AgentResponse(BaseModel):
    """ответ на данные агента"""
    id: str
    user_id: str
    name: str
    hostname: str
    public_ip: Optional[str]
    local_ip: Optional[str]
    status: str
    version: str
    last_seen: Optional[datetime]
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True


class AgentUpdate(BaseModel):
    """обнавление агента"""

    name: Optional[str] = None
    public_ip: Optional[str] = None
    local_ip: Optional[str] = None
    version: Optional[str] = None   

class AgentHeartbeat(BaseModel):

    hostname: str
    public_ip: str
    local_ip: Optional[str]
    version: Optional[str] = "1.0.0"
    status: Literal[StatusType.ONLINE, StatusType.OFFLINE, StatusType.ERROR] = StatusType.ONLINE
    


