from fastcrud import crud_router
from fastapi import Depends

from ...core.db.database import async_get_db
from ...models.job_skill import JobSkill
from ...schemas.job_skill import JobSkillCreate, JobSkillUpdate
from ..dependencies import get_current_superuser

router = crud_router(
    session=async_get_db,
    model=JobSkill,
    create_schema=JobSkillCreate,
    update_schema=JobSkillUpdate,
    path="/job-skill",
    tags=["Job Skill"],
    create_deps=[Depends(get_current_superuser)],
    update_deps=[Depends(get_current_superuser)],
    delete_deps=[Depends(get_current_superuser)],
    db_delete_deps=[Depends(get_current_superuser)],
)
