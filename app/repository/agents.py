from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.agent import Agent
from app.models.user import User
from app.schemas.agent import AgentResponse, AgentCreate

async def create_agent(
    db: AsyncSession,
    user_id: int,
    name: str,
    hostname: str,
    public_ip: str,
    local_ip: str,
    status: str,
    version: str,
) -> Agent:
    
    agent = Agent(
    user_id=user_id,
    name=name,
    hostname=hostname,
    public_ip=public_ip,
    local_ip=local_ip,
    status=status,
    version=version,
    )
    
    await db.add(agent)
    await db.flush()
    return agent

async def agent_exists(
    db: AsyncSession,
    current_user: User,
    agent_id: str,
) -> bool:
    """
    проверить, существует ли агент с таким ID у пользователя.
    """
    stmt = select(Agent).where(
        Agent.id == agent_id,
        Agent.user_id == current_user.id
    )
    result = await db.execute(stmt)
    return result.scalar_one_or_none() is not None

async def get_agents(
    db: AsyncSession,
    user_id: int,
    limit: int = 100,
    offset: int = 0,
) -> list[Agent]:
    
    """
    получить список агентов текущего пользователя.
    """

    stmt = select(Agent).where(Agent.user_id == user_id).limit(limit).offset(offset)
    result = await db.execute(stmt)
    return result.scalars().all()


async def get_agent_by_id_repo(
        agent_id: int, 
        db: AsyncSession, 
        user_id: int
) -> AgentResponse:
    
    stmt = select(Agent).where(Agent.id == agent_id, Agent.user_id == user_id)
    result = await db.execute(stmt)

    return result.scalars().all()
