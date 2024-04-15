from fastcrud import crud_router
from fastapi import Depends

from ...core.db.database import async_get_db
from ...models.skill import Skill
from ...schemas.skill import SkillCreate, SkillUpdate
from ..dependencies import get_current_superuser

router = crud_router(
    session=async_get_db,
    model=Skill,
    create_schema=SkillCreate,
    update_schema=SkillUpdate,
    path="/skill",
    tags=["Skill"],
    create_deps=[Depends(get_current_superuser)],
    update_deps=[Depends(get_current_superuser)],
    delete_deps=[Depends(get_current_superuser)],
    db_delete_deps=[Depends(get_current_superuser)],
)
