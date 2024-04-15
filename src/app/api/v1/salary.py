from fastcrud import crud_router
from fastapi import Depends

from ...core.db.database import async_get_db
from ...models.salary import Salary
from ...schemas.salary import SalaryCreate, SalaryUpdate
from ..dependencies import get_current_superuser

router = crud_router(
    session=async_get_db,
    model=Salary,
    create_schema=SalaryCreate,
    update_schema=SalaryUpdate,
    path="/salary",
    tags=["Salary"],
    create_deps=[Depends(get_current_superuser)],
    update_deps=[Depends(get_current_superuser)],
    delete_deps=[Depends(get_current_superuser)],
    db_delete_deps=[Depends(get_current_superuser)],
)
