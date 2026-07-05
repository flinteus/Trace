from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException, status
from sqlalchemy import select

from app.models.user import User
from app.models.agent import Agent
from app.repository import agents as agent_repo
from app.schemas.agent import AgentCreate

async def register_agent(
    db: AsyncSession,
    current_user: User,
    agent_data: AgentCreate,  
) -> Agent:
    """
    Бизнес-логика для регистрации нового агента.
    """
    # проверяем, не существует ли уже агент с таким hostname у этого пользователя
    stmt = select(Agent).where(
        Agent.hostname == agent_data.hostname,
        Agent.user_id == current_user.id
    )
    result = await db.execute(stmt)
    existing_agent = result.scalar_one_or_none()

    if existing_agent:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Agent with hostname '{agent_data.hostname}' already exists"
        )

    new_agent = agent_repo.create_agent(
        db=db,
        user_id=current_user.id,
        name=agent_data.name or agent_data.hostname,
        hostname=agent_data.hostname,
        public_ip=agent_data.public_ip,
        local_ip=agent_data.local_ip,
        status="offline",  # при создании ставим статус offline
        version=agent_data.version or "1.0.0",
    )

    await db.commit()
    await db.refresh(new_agent)  # обновляем объект из БД (получаем id, created_at и т.д.)

    return new_agent


async def get_agents(
    db: AsyncSession,
    current_user: User,
    limit: int = 100,
    offset: int = 0,  
) -> list[Agent]:
    
        return await agent_repo.get_agents(db, current_user.id, limit, offset)

