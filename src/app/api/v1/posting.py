from fastcrud import crud_router

from ...core.db.database import async_get_db
from ...models.posting import Posting
from ...schemas.posting import PostingCreate, PostingUpdate

router = crud_router(
    session=async_get_db,
    model=Posting,
    create_schema=PostingCreate,
    update_schema=PostingUpdate,
    path="/posting",
    tags=["Posting"]
)
