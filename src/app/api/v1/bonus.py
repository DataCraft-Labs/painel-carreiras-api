from fastcrud import crud_router

from ...core.db.database import async_get_db
from ...models.bonus import Bonus
from ...schemas.bonus import BonusCreate, BonusUpdate

router = crud_router(
    session=async_get_db,
    model=Bonus,
    create_schema=BonusCreate,
    update_schema=BonusUpdate,
    path="/bonus",
    tags=["Bonus"]
)
