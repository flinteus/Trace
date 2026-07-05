from sqlalchemy.orm import Session

from app.models.agent import Agent

def create_agent(
    db: Session,
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
    
    db.add(agent)
    db.flush()
    return agent
