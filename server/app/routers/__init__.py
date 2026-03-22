from fastapi import APIRouter
from .admin import router as admin_router
from .application import router as application_router
from .auth import router as auth_router
from .event import router as event_router
from .hackathon import router as hackathon_router
from .room import router as room_router
from .team import router as team_router
from .team_request import router as team_request_router
from .user import router as user_router

router = APIRouter()
router.include_router(admin_router)
router.include_router(application_router)
router.include_router(auth_router)
router.include_router(event_router)
router.include_router(hackathon_router)
router.include_router(room_router)
router.include_router(team_router)
router.include_router(team_request_router)
router.include_router(user_router)
