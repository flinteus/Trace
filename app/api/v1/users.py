from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from pydantic import UUID4

from app.database.db import UserModel
from app.models import ErrorMessage
from app.services.auth import get_current_user
from app.services.business_logic import roles
from app.services.users import get_user

router = APIRouter()

@router.get(
    "/me",
    summary="Get current user info",
    description="Get information about the currently authenticated user",
    response_model=UserModel,
    responses={
        200: {"description": "User information"},
        401: {"model": ErrorMessage, "description": "Invalid or missing token"},
    },
)
async def get_user_info(user_uid: UUID4 = Depends(get_current_user)):
    """Get current user information from JWT token."""
    return jsonable_encoder(get_user(user_uid))


@router.get(
    "/admin",
    summary="For admin only",
    responses={
        200: {"description": "Admin information"},
        403: {"model": ErrorMessage, "description": "Access forbidden"},
    },
)
@roles({"admin"})
async def admin_handler(user_uid: UUID4 = Depends(get_current_user)):
    """Admin-only endpoint."""
    return {"message": "It's for admin only!", "user_uid": user_uid}
