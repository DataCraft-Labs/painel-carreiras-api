from fastcrud import crud_router

from ...core.db.database import async_get_db
from ...models.benefit import Benefit
from ...schemas.benefit import BenefitsCreate, BenefitsUpdate

router = crud_router(
    session=async_get_db,
    model=Benefit,
    create_schema=BenefitsCreate,
    update_schema=BenefitsUpdate,
    path="/benefit",
    tags=["Benefit"]
)
