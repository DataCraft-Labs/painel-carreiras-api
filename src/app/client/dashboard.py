from typing import Annotated
import statistics

from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, distinct, func


from .config import templates
from ..models.position import Position
from ..models.posting import Posting
from ..models.salary import Salary
from ..core.db.database import async_get_db

router = APIRouter(tags=["client_dashboard"])

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


@router.get("/salary_distribution/")
async def get_salary_distribution(
    position: str,
    db: AsyncSession = Depends(async_get_db)
):
    query = select(
        Salary.base_salary.label('salary'),
        func.count().label('count')
    ).join(
        Posting, Posting.id == Salary.posting_id
    ).join(
        Position, Position.id == Posting.position_id
    ).where(
        func.lower(Position.title).like(f"%{position.lower()}%")
    ).group_by(
        Salary.base_salary
    ).order_by(
        Salary.base_salary
    )

    result = await db.execute(query)
    salaries = result.all()
    if not salaries:
        raise HTTPException(status_code=404, detail="No salary data found for the given position.")
    
    salary_list = [salary for salary, count in salaries for _ in range(count)]
    mean_salary = statistics.mean(salary_list) if salary_list else 0
    median_salary = statistics.median(salary_list) if salary_list else 0
    std_deviation = statistics.stdev(salary_list) if len(salary_list) > 1 else 0

    salary_distribution = {
        'salaries': [{'salary': salary, 'count': count} for salary, count in salaries],
        'statistics': {
            'mean': mean_salary,
            'median': median_salary,
            'std_deviation': std_deviation
        }
    }
    return salary_distribution
