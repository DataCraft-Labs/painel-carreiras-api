from fastapi import APIRouter

from .login import router as login_router
from .logout import router as logout_router
from .rate_limits import router as rate_limits_router
from .users import router as users_router
from .position import router as position_router
from .posting import router as posting_router
from .salary import router as salary_router
from .skill import router as skill_router
from .job_skill import router as job_skill_router
from .benefit import router as benefits_router
from .bonus import router as bonus_router
from .equity import router as equity_router
from .scraper import router as scraper_router


router = APIRouter(prefix="/v1")
router.include_router(login_router)
router.include_router(logout_router)
router.include_router(users_router)
router.include_router(rate_limits_router)
router.include_router(position_router)
router.include_router(posting_router)
router.include_router(salary_router)
router.include_router(skill_router)
router.include_router(job_skill_router)
router.include_router(benefits_router)
router.include_router(bonus_router)
router.include_router(equity_router)
router.include_router(scraper_router)
