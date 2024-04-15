from fastcrud import crud_router

from ...core.db.database import async_get_db
from ...models.position import Position
from ...schemas.position import PositionCreate, PositionUpdate

router = crud_router(
    session=async_get_db,
    model=Position,
    create_schema=PositionCreate,
    update_schema=PositionUpdate,
    path="/position",
    tags=["Position"]
)
