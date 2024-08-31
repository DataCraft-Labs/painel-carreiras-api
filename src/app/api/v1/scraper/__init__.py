from fastapi import APIRouter

from .scraper import router as scraper_router

router = APIRouter(prefix="/v1")
router.include_router(scraper_router)
