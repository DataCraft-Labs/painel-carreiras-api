from typing import Annotated

from fastcrud import FastCRUD
from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse, JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, distinct

from .config import templates
from ..models.position import Position
from ..models.posting import Posting
from ..core.db.database import async_get_db

router = APIRouter(tags=["client_dashboard"])

crud = FastCRUD(Position)

@router.get("/dashboard", response_class=HTMLResponse)
async def get_dashboard(request: Request):
    return templates.TemplateResponse(
            "dashboard.html",
            {
                "request": request,
            },
        )


@router.get("/dropdown_data", response_class=HTMLResponse)
async def get_dropdown(request: Request, db: Annotated[AsyncSession, Depends(async_get_db)]):
    positions = await db.execute(select(distinct(Position.title)))
    locations = await db.execute(select(distinct(Posting.location)))
    companies = await db.execute(select(distinct(Posting.company)))
    
    positions_html = "".join(f'<option value="{row[0]}">{row[0]}</option>' for row in positions.fetchall())
    locations_html = "".join(f'<option value="{row[0]}">{row[0]}</option>' for row in locations.fetchall())
    companies_html = "".join(f'<option value="{row[0]}">{row[0]}</option>' for row in companies.fetchall())
    
    return HTMLResponse(content=f"""
        <script>
            document.getElementById('position-select').innerHTML = '<option value="">Select a position...</option>{positions_html}';
            document.getElementById('location-select').innerHTML = '<option value="">Select a location...</option>{locations_html}';
            document.getElementById('company-select').innerHTML = '<option value="">Select a company...</option>{companies_html}';
        </script>
    """)
