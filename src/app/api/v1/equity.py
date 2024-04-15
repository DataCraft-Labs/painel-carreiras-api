from fastcrud import crud_router

from ...core.db.database import async_get_db
from ...models.equity import Equity
from ...schemas.equity import EquityCreate, EquityUpdate

router = crud_router(
    session=async_get_db,
    model=Equity,
    create_schema=EquityCreate,
    update_schema=EquityUpdate,
    path="/equity",
    tags=["Equity"]
)
