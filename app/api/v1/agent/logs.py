from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.models.user import User
from app.services import agents as agent_servise
from app.schemas.agent import AgentResponse, AgentUpdate, AgentHeartbeat
from app.dependecy import get_current_user 



router = APIRouter(tags=["Logs"])

@router.get("/api/v1/agents/{agent_id}/logs")
async def get_all_logs(
    agent_id: int,
    db: AsyncSession = Depends(get_db), 
    current_user: User = Depends(get_current_user),
):
    """список доступных лог-файлов на агенте"""
    ...

@router.get("/api/v1/agents/{agent_id}/logs/{log_name}")
async def get_log(
    log_name: str,
    agent_id: int,
    db: AsyncSession = Depends(get_db), 
    current_user: User = Depends(get_current_user),
):
    """получить содержимое конкретного лога"""
    ...

@router.get("/api/v1/agents/{agent_id}/logs/{log_name}/tail")
async def get_last_logs(
    log_name: str,
    agent_id: int,
    db: AsyncSession = Depends(get_db), 
    current_user: User = Depends(get_current_user),
):
    """последние n строк лога"""
    ...

@router.websocket("/ws/agents/{agent_id}/logs/{log_name}")
async def ws_logs(
    log_name: str,
    agent_id: int,
    db: AsyncSession = Depends(get_db), 
    current_user: User = Depends(get_current_user),
):
    """стриминг логов в реальном времени """
    ...
