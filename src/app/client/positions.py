from typing import Annotated
from math import ceil

from fastcrud import FastCRUD
from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

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


    template = "positions/positions.html"
    if "HX-Request" in request.headers:
        template = "positions/positions_table.html"
    
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


@router.get("/search_positions", response_class=HTMLResponse)
async def search_positions(request: Request, db: Annotated[AsyncSession, Depends(async_get_db)], search: str = "", page: int = 1):
    limit = int(request.query_params.get("rows-per-page-select", 10))
    offset = (page - 1) * limit

    query = select(Position).offset(offset).limit(limit)
    if search:
        query = query.where(Position.title.ilike(f"%{search}%"))

    positions_result = await db.execute(query)
    positions = positions_result.scalars().all()

    total_count_query = select(func.count()).select_from(Position)
    if search:
        total_count_query = total_count_query.where(Position.title.ilike(f"%{search}%"))
    total_count_result = await db.execute(total_count_query)
    total_count = total_count_result.scalar_one()

    total_pages = ceil(total_count / limit)

    return templates.TemplateResponse(
        "positions/positions_table.html", 
        {
            "request": request,
            "positions": positions,
            "total_items": total_count,
            "current_page": page,
            "total_pages": total_pages,
            "rows_per_page": limit
        }
    )
