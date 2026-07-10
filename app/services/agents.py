import datetime
import logging

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException, status
from sqlalchemy import select

from app.models.user import User
from app.models.agent import Agent
from app.models.enum import StatusType
from app.repository import agents as agent_repo
from app.schemas.agent import AgentCreate, AgentResponse, AgentUpdate, AgentHeartbeat

logger = logging.getLogger(__name__)

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

        logger.warning(
            f"User {current_user.id} tried to register duplicate agent: {agent_data.hostname}"
        )
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

    logger.info(
        f"Agent registered successfully: id={new_agent.id}, hostname={new_agent.hostname}, "
        f"user={current_user.id}"
    )
    return new_agent


async def get_agents(
    db: AsyncSession,
    current_user: User,
    limit: int = 100,
    offset: int = 0,  
) -> list[Agent]:
     
    logger.debug(f"User {current_user.id} requested agents list (limit={limit}, offset={offset})")
    return await agent_repo.get_agents(db, current_user.id, limit, offset)

async def get_agent_by_id(
    agent_id: int,
    db: AsyncSession,
    user_id: int,
) -> AgentResponse:
    logger.debug(f"User {user_id} requested agent {agent_id}")
     
    stmt = select(Agent).where(
        Agent.id == agent_id,
        Agent.user_id == user_id
    )
    result = await db.execute(stmt)
    existing_agent = result.scalar_one_or_none()

    if existing_agent:
        logger.warning(f"User {user_id} requested non-existent agent {agent_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Agent with id '{agent_id}' not fuond"
        )
     
    return await agent_repo.get_agent_by_id_repo(agent_id, db, user_id)


async def put_agent(
    agent_id: int,
    agent_data: AgentUpdate,
    db: AsyncSession, 
    user_id: int,
) -> Agent:
    logger.info(f"User {user_id} updating agent {agent_id}")
        
    stmt = select(Agent).where(
    Agent.id == agent_id,
    Agent.user_id == user_id
    )
    result = await db.execute(stmt)
    existing_agent = result.scalar_one_or_none()

    if existing_agent:
        logger.warning(f"User {user_id} tried to update non-existent agent {agent_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Agent not found or access denied"
        )
    
    update_data = agent_data.model_dump(exclude_unset=True)
    
    for key, value in update_data.items():
        if hasattr(existing_agent, key):
            setattr(existing_agent, key, value)
    
    
    await db.commit()
    await db.refresh(existing_agent)
    
    logger.info(f"Agent {agent_id} updated by user {user_id}. New data: {update_data}")
    return existing_agent


async def del_agent(
    db: AsyncSession,
    user_id: str,
    agent_id: str,
) -> None:
    logger.info(f"User {user_id} attempting to delete agent {agent_id}")

    stmt = select(Agent).where(
        Agent.id == agent_id,
        Agent.user_id == user_id
    )
    result = await db.execute(stmt)
    agent = result.scalar_one_or_none()
    
    if not agent:
        logger.warning(f"User {user_id} tried to delete non-existent agent {agent_id}")

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Agent not found or access denied"
        )

    await db.delete(agent)

    await db.commit()

    logger.info(f"Agent {agent_id} deleted by user {user_id}")

async def process_heartbeat(
    db: AsyncSession,
    user_id: str,
    heartbeat_data: AgentHeartbeat,
):
    logger.debug(f"Heartbeat received from {heartbeat_data.hostname} (user {user_id})")

    stmt = select(Agent).where(
        Agent.hostname == heartbeat_data.hostname,
        Agent.user_id == user_id
    )

    result = await db.execute(stmt)
    agent = result.scalar_one_or_none()

    if not agent:
        logger.warning(f"Heartbeat from unknown hostname: {heartbeat_data.hostname}")

        agent = await agent_repo.create_agent(
            db=db,
            user_id=user_id,
            name=heartbeat_data.hostname,
            hostname=heartbeat_data.hostname,
            public_ip=heartbeat_data.public_ip,
            local_ip=heartbeat_data.local_ip,
            status=StatusType.ONLINE,
            version=heartbeat_data.version,
        )
        await db.commit()
        await db.refresh(agent)

        logger.info(f"New agent registered via heartbeat: id={agent.id}")
        return agent
    
    agent.public_ip = heartbeat_data.public_ip
    agent.local_ip = heartbeat_data.local_ip or agent.local_ip
    agent.version = heartbeat_data.version
    agent.status = heartbeat_data.status
    agent.last_seen = datetime.utcnow()
    
    await db.commit()
    await db.refresh(agent)

    logger.debug(f"Heartbeat processed for agent {agent.id} (status: {agent.status})")
    return agent


