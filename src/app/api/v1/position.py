from fastcrud import crud_router
from fastapi import Depends

from ...core.db.database import async_get_db
from ...models.position import Position
from ...schemas.position import PositionCreate, PositionUpdate
from ..dependencies import get_current_superuser

router = crud_router(
    session=async_get_db,
    model=Position,
    create_schema=PositionCreate,
    update_schema=PositionUpdate,
    path="/position",
    tags=["Position"],
    create_deps=[Depends(get_current_superuser)],
    update_deps=[Depends(get_current_superuser)],
    delete_deps=[Depends(get_current_superuser)],
    db_delete_deps=[Depends(get_current_superuser)],
)
