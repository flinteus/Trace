from fastapi import APIRouter
from .auth import router as auth_router
from .users import router as users_router
from .health import router as health_router
from .protected import router as protected_router
from .agent import agents_router_registr, agents_router

router = APIRouter()

router.include_router(auth_router, prefix="/auth", tags=["Authentication"])
router.include_router(users_router, prefix="/users", tags=["Users"])
router.include_router(health_router, prefix="", tags=["Health"])
router.include_router(protected_router, prefix="", tags=["Protected"])
router.include_router(agents_router_registr)
router.include_router(agents_router)
