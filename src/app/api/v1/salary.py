from fastcrud import crud_router

from ...core.db.database import async_get_db
from ...models.salary import Salary
from ...schemas.salary import SalaryCreate, SalaryUpdate

router = crud_router(
    session=async_get_db,
    model=Salary,
    create_schema=SalaryCreate,
    update_schema=SalaryUpdate,
    path="/salary",
    tags=["Salary"]
)
