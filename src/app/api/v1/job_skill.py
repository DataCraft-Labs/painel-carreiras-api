from fastcrud import crud_router

from ...core.db.database import async_get_db
from ...models.job_skill import JobSkill
from ...schemas.job_skill import JobSkillCreate, JobSkillUpdate

router = crud_router(
    session=async_get_db,
    model=JobSkill,
    create_schema=JobSkillCreate,
    update_schema=JobSkillUpdate,
    path="/job-skill",
    tags=["Job Skill"]
)
