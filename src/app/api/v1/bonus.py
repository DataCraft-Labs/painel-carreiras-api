from fastcrud import crud_router
from fastapi import Depends

from ...core.db.database import async_get_db
from ...models.bonus import Bonus
from ...schemas.bonus import BonusCreate, BonusUpdate
from ..dependencies import get_current_superuser

router = crud_router(
    session=async_get_db,
    model=Bonus,
    create_schema=BonusCreate,
    update_schema=BonusUpdate,
    path="/bonus",
    tags=["Bonus"],
    create_deps=[Depends(get_current_superuser)],
    update_deps=[Depends(get_current_superuser)],
    delete_deps=[Depends(get_current_superuser)],
    db_delete_deps=[Depends(get_current_superuser)],
)
