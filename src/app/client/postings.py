from typing import Annotated
from math import ceil

from fastcrud import FastCRUD
from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from .config import templates
from ..models.posting import Posting
from ..core.db.database import async_get_db

router = APIRouter(tags=["client_postings"])
crud = FastCRUD(Posting)

@router.get("/postings", response_class=HTMLResponse)
async def get_postings(request: Request, db: Annotated[AsyncSession, Depends(async_get_db)]):
    page = int(request.query_params.get("page", 1))
    limit = int(request.query_params.get("rows-per-page-select", 10))
    offset = (page - 1) * limit

    postings = await crud.get_multi(db=db, offset=offset, limit=limit)
    total_pages = ceil(postings["total_count"] / limit)

    template = "postings.html"
    if "HX-Request" in request.headers:
        template = "postings_table.html"
    
    return templates.TemplateResponse(
            template,
            {
                "request": request,
                "postings": postings["data"],
                "total_items": postings["total_count"],
                "current_page": page,
                "total_pages": total_pages,
                "rows_per_page": limit
            },
        )


@router.get("/search_postings", response_class=HTMLResponse)
async def search_postings(request: Request, db: Annotated[AsyncSession, Depends(async_get_db)], search: str = "", page: int = 1):
    limit = int(request.query_params.get("rows-per-page-select", 10))
    offset = (page - 1) * limit

    query = select(Posting).offset(offset).limit(limit)
    if search:
        query = query.where(Posting.original_title.ilike(f"%{search}%"))

    postings_result = await db.execute(query)
    postings = postings_result.scalars().all()

    total_count_query = select(func.count()).select_from(Posting)
    if search:
        total_count_query = total_count_query.where(Posting.original_title.ilike(f"%{search}%"))
    total_count_result = await db.execute(total_count_query)
    total_count = total_count_result.scalar_one()

    total_pages = ceil(total_count / limit)

    return templates.TemplateResponse(
        "postings_table.html", 
        {
            "request": request,
            "postings": postings,
            "total_items": total_count,
            "current_page": page,
            "total_pages": total_pages,
            "rows_per_page": limit
        }
    )
