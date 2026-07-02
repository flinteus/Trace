from fastapi import APIRouter, Depends
from app.services.auth import get_current_user

router = APIRouter()

@router.get("/protected")
async def protected_route(username: str = Depends(get_current_user)):
    """
    Protected route that requires a valid JWT token.
    Returns a simple message with the authenticated user.
    """
    return {
        "message": "This is a protected route",
        "data": "secret information accessible with JWT token",
        "authenticated_user": username,
    }
