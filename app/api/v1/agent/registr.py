from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.models.user import User
from app.services import agents as agent_servise
from app.schemas.agent import AgentCreate
from app.dependecy import get_current_user 

router = APIRouter()

@router.post("/registr")
async def create_server(
    agent_data: AgentCreate,
    db: AsyncSession = Depends(get_db), 
    current_user: User = Depends(get_current_user),  
):
    return await agent_servise.register_agent(db, current_user, agent_data)
    


