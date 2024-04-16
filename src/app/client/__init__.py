from fastapi import APIRouter

from .login import router as login_router
from .positions import router as positions_router
from .postings import router as postings_router
from .landing import router as landing_router

router = APIRouter()
router.include_router(login_router)
router.include_router(positions_router)
router.include_router(postings_router)
router.include_router(landing_router)
