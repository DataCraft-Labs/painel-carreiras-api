from fastcrud import crud_router
from fastapi import Depends

from ...core.db.database import async_get_db
from ...models.equity import Equity
from ...schemas.equity import EquityCreate, EquityUpdate
from ..dependencies import get_current_superuser

router = crud_router(
    session=async_get_db,
    model=Equity,
    create_schema=EquityCreate,
    update_schema=EquityUpdate,
    path="/equity",
    tags=["Equity"],
    create_deps=[Depends(get_current_superuser)],
    update_deps=[Depends(get_current_superuser)],
    delete_deps=[Depends(get_current_superuser)],
    db_delete_deps=[Depends(get_current_superuser)],
)
