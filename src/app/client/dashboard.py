from typing import Annotated
import statistics

from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, distinct, func, and_
import numpy as np
import pandas as pd

from .config import templates
from ..models.position import Position
from ..models.posting import Posting
from ..models.salary import Salary
from ..models.skill import Skill
from ..models.job_skill import JobSkill
from ..core.db.database import async_get_db

router = APIRouter(tags=["client_dashboard"])

def format_salary_range(interval):
    lower, upper = interval.left // 1000, interval.right // 1000
    lower_str = f"{int(lower)}K"
    upper_str = f"{int(upper)}K"
    return f"{lower_str} - {upper_str}"

@router.get("/dashboard", response_class=HTMLResponse)
async def get_dashboard(request: Request):
    return templates.TemplateResponse(
            "dashboard/dashboard.html",
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
    position: str = '',
    location: str = '',
    company: str = '',
    db: AsyncSession = Depends(async_get_db)
):
    conditions = []
    if position:
        conditions.append(func.lower(Position.title).like(f"%{position.lower()}%"))
    if location:
        conditions.append(func.lower(Posting.location).like(f"%{location.lower()}%"))
    if company:
        conditions.append(func.lower(Posting.company).like(f"%{company.lower()}%"))

    query = select(
        Salary.base_salary.label('salary'),
        func.count().label('count')
    ).join(
        Posting, Posting.id == Salary.posting_id
    ).join(
        Position, Position.id == Posting.position_id
    )

    if conditions:
        query = query.where(and_(*conditions))

    query = query.group_by(
        Salary.base_salary
    ).order_by(
        Salary.base_salary
    )

    result = await db.execute(query)
    salaries = result.all()
    if not salaries:
        raise HTTPException(status_code=404, detail="No salary data found for the given criteria.")
    
    salary_list = [float(salary) for salary, count in salaries for _ in range(count)]
    num_bins = min(int(np.ceil(np.log2(len(salary_list)) + 1)), 7)

    bin_edges = np.linspace(min(salary_list), max(salary_list), num_bins + 1)
    salary_df = pd.DataFrame(salary_list, columns=['salary'])
    salary_df['binned'] = pd.cut(salary_df['salary'], bins=bin_edges, include_lowest=True)
    salary_counts = salary_df['binned'].value_counts().sort_index()

    salary_distribution = {
        'salaries': [{'salary': format_salary_range(salary), 'count': count} for salary, count in salary_counts.items()],
        'statistics': {
            'mean': str(int(statistics.mean(salary_list) / 1000)) + 'k' if salary_list else 0,
            'median': str(int(statistics.median(salary_list) / 1000)) + 'k' if salary_list else 0,
            'std_deviation': int(statistics.stdev(salary_list)) if len(salary_list) > 1 else 0
        }
    }
    return salary_distribution


@router.get("/top_used_skills")
async def get_top_used_skills(
    position: str = '',
    location: str = '',
    company: str = '',
    db: AsyncSession = Depends(async_get_db)
):
    conditions = []
    if position:
        conditions.append(func.lower(Position.title).like(f"%{position.lower()}%"))
    if location:
        conditions.append(func.lower(Posting.location).like(f"%{location.lower()}%"))
    if company:
        conditions.append(func.lower(Posting.company).like(f"%{company.lower()}%"))

    total_skills_query = select(
        func.count(JobSkill.skill_id)
    ).join(
        Posting, Posting.id == JobSkill.posting_id
    ).join(
        Position, Position.id == Posting.position_id
    )

    if conditions:
        total_skills_query = total_skills_query.where(and_(*conditions))

    total_skills_result = await db.execute(total_skills_query)
    total_skills = total_skills_result.scalar()

    query = select(
        Skill.name.label('name'),
        func.count(JobSkill.skill_id).label('count')
    ).join(
        JobSkill, Skill.id == JobSkill.skill_id
    ).join(
        Posting, Posting.id == JobSkill.posting_id
    ).join(
        Position, Position.id == Posting.position_id
    )

    if conditions:
        query = query.where(and_(*conditions))

    query = query.group_by(
        Skill.name
    ).order_by(
        func.count(JobSkill.skill_id).desc()
    ).limit(5)

    result = await db.execute(query)
    skills = result.all()
    
    if not skills:
        raise HTTPException(status_code=404, detail="No skill data found for the given criteria.")

    return {
        'skills': [{'name': skill, 'percentage': (count / total_skills) * 100} for skill, count in skills]
    }
