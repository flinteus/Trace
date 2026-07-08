from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.models.user import User
from app.services import agents as agent_servise
from app.schemas.agent import AgentResponse, AgentUpdate, AgentHeartbeat
from app.dependecy import get_current_user 

router = APIRouter(tags=["Agents"])

@router.get("/agents")
async def get_all_agents(
    db: AsyncSession = Depends(get_db), 
    current_user: User = Depends(get_current_user),  
):
    return await agent_servise.get_agents(db, current_user)

@router.get("/agents/{agent_id}", response_model=AgentResponse)
async def get_agent(
    agent_id: str,
    db: AsyncSession = Depends(get_db), 
    current_user: User = Depends(get_current_user),
) -> AgentResponse:
    
    return await agent_servise.get_agent_by_id(agent_id, db, current_user.id)

@router.put("/agents/{agent_id}", response_model=AgentResponse)
async def put_agent(
    agent_id: str,
    agent_data: AgentUpdate,
    db: AsyncSession = Depends(get_db), 
    current_user: User = Depends(get_current_user),
) -> AgentResponse:
    
    return await agent_servise.put_agent(agent_id, agent_data, db, current_user.id)
    
@router.delete("/agents/{agent_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_agent(
    agent_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> None:
    
    await agent_servise.del_agent(db, current_user.id, agent_id)

@router.post("/heartbeat", response_model=AgentResponse)
async def process_heartbeat(
    heartbeat_data: AgentHeartbeat,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> AgentResponse:

    return await agent_servise.process_heartbeat(db, current_user.id, heartbeat_data)

