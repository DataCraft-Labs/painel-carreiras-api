from fastcrud import crud_router
from fastapi import Depends

from ...core.db.database import async_get_db
from ...models.posting import Posting
from ...schemas.posting import PostingCreate, PostingUpdate
from ..dependencies import get_current_superuser

router = crud_router(
    session=async_get_db,
    model=Posting,
    create_schema=PostingCreate,
    update_schema=PostingUpdate,
    path="/posting",
    tags=["Posting"],
    # create_deps=[Depends(get_current_superuser)],
    # update_deps=[Depends(get_current_superuser)],
    # delete_deps=[Depends(get_current_superuser)],
    # db_delete_deps=[Depends(get_current_superuser)],
)
