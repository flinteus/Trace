from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.models.user import User

router = APIRouter()

@router.post("/registr")
async def create_server(
    db: AsyncSession = Depends(get_db), 
    current_user: User, 
    name: str, 
    hostname: str, 
    public_ip: str | None,
    local_ip: str | None,
    version: str | None,  
):
    


