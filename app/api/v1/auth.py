from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.security import HTTPAuthorizationCredentials

from app.models.auth import (
    LoginRequest,
    LoginResponse,
    RefreshTokenRequest,
    RefreshTokenResponse,
    RegistrationRequest,
    ErrorMessage,
)
from app.services.auth import (
    get_current_user,
    blacklist_token,
    security,
    generate_refresh_token,
)
from app.services.business_logic import register_new_user, authorize

router = APIRouter()

@router.post(
    "/login",
    response_model=LoginResponse,
    summary="Login with username and password",
    description="Get JWT access and refresh tokens",
    responses={
        200: {"description": "Login successful"},
        401: {"model": ErrorMessage, "description": "Invalid credentials"},
    },
)
async def login(login_request: LoginRequest):
    """Login endpoint that returns both access and refresh tokens."""
    return jsonable_encoder(authorize(login_request))


@router.post(
    "/refresh",
    response_model=RefreshTokenResponse,
    summary="Refresh access token",
    description="Get a new access token using a valid refresh token",
    responses={
        200: {"description": "Token refreshed successfully"},
        401: {"model": ErrorMessage, "description": "Invalid or expired refresh token"},
    },
)
async def refresh_token_handler(refresh_request: RefreshTokenRequest):
    """Refresh endpoint that generates a new access token using a refresh token."""
    return generate_refresh_token(refresh_request.refresh_token)


@router.post(
    "/logout",
    summary="Logout and blacklist tokens",
    description="Blacklist the current JWT token",
    responses={
        200: {"description": "Logout successful"},
        401: {"model": ErrorMessage, "description": "Invalid or missing token"},
    },
)
async def logout(
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    """Logout endpoint that blacklists the current JWT token."""
    access_token = credentials.credentials
    blacklist_token(access_token)
    return {"message": "Logout successful"}


@router.post(
    "/registration",
    response_model=RefreshTokenResponse,
    summary="Register new user",
    description="Register new user and get a new access token",
    responses={
        201: {"description": "User registered successfully"},
    },
)
async def register_new_user_handler(
    request: RegistrationRequest,
) -> RefreshTokenResponse:
    """Register new user."""
    return jsonable_encoder(register_new_user(request))
