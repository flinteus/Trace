from sqlalchemy import Column, String, DateTime, Boolean, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base
import uuid

class Agent(Base):
    __tablename__ = "agents"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    name = Column(String(100))
    hostname = Column(String(255), unique=True, nullable=False)
    public_ip = Column(String(45))
    local_ip = Column(String(45))
    status = Column(String(20), default="offline")  # online, offline, error
    version = Column(String(20), default="1.0.0")
    last_seen = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # cвязь с пользователем (один пользователь -> много агентов)
    user = relationship("User", backref="agents")

