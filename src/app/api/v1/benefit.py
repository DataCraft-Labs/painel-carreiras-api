from fastcrud import crud_router
from fastapi import Depends

from ...core.db.database import async_get_db
from ...models.benefit import Benefit
from ...schemas.benefit import BenefitsCreate, BenefitsUpdate
from ..dependencies import get_current_superuser

router = crud_router(
    session=async_get_db,
    model=Benefit,
    create_schema=BenefitsCreate,
    update_schema=BenefitsUpdate,
    path="/benefit",
    tags=["Benefit"],
    create_deps=[Depends(get_current_superuser)],
    update_deps=[Depends(get_current_superuser)],
    delete_deps=[Depends(get_current_superuser)],
    db_delete_deps=[Depends(get_current_superuser)],
)
