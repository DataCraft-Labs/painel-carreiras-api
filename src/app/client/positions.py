from typing import Annotated
from math import ceil

from fastcrud import FastCRUD
from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from sqlalchemy.ext.asyncio import AsyncSession

from .config import templates
from ..models.position import Position
from ..core.db.database import async_get_db

router = APIRouter(tags=["client_positions"])
crud = FastCRUD(Position)

@router.get("/positions", response_class=HTMLResponse)
async def get_positions(request: Request, db: Annotated[AsyncSession, Depends(async_get_db)]):
    page = int(request.query_params.get("page", 1))
    limit = int(request.query_params.get("rows-per-page-select", 10))
    offset = (page - 1) * limit

    positions = await crud.get_multi(db=db, offset=offset, limit=limit)
    
    total_pages = ceil(positions["total_count"] / limit)


    template = "positions.html"
    if "HX-Request" in request.headers:
        template = "positions_table.html"
    
    return templates.TemplateResponse(
            template,
            {
                "request": request,
                "positions": positions["data"],
                "total_items": positions["total_count"],
                "current_page": page,
                "total_pages": total_pages,
                "rows_per_page": limit
            },
        )
