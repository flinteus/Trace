from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.models.user import User
from app.services import agents as agent_servise
from app.schemas.agent import AgentResponse
from app.dependecy import get_current_user 

router = APIRouter()

@router.get("/agents")
async def get_all_agents(
    db: AsyncSession = Depends(get_db), 
    current_user: User = Depends(get_current_user),  
):
    return await agent_servise.get_agents(db, current_user)

@router.get("/agents/{agent_id}")
async def get_agent(
    agent_id: int,
    db: AsyncSession = Depends(get_db), 
    current_user: User = Depends(get_current_user),
) -> AgentResponse:
    
    return await agent_servise.get_agent_by_id(db, current_user.id)
    
