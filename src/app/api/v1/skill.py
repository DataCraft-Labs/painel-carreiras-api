from fastcrud import crud_router

from ...core.db.database import async_get_db
from ...models.skill import Skill
from ...schemas.skill import SkillCreate, SkillUpdate

router = crud_router(
    session=async_get_db,
    model=Skill,
    create_schema=SkillCreate,
    update_schema=SkillUpdate,
    path="/skill",
    tags=["Skill"]
)
