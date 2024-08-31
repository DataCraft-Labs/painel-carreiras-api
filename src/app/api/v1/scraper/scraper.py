from typing import Annotated

from sqlalchemy.orm import Session
from sqlalchemy import text
from fastapi import APIRouter, Depends, HTTPException
from typing import Any, Optional
from fastcrud import FastCRUD
from arq.jobs import Job as ArqJob
from sqlalchemy.ext.asyncio import AsyncSession


from .helper import scrape_endpoint
from ....core.utils import queue
from ....api.dependencies import async_get_db
from ....models.position import Position
from ....models.posting import Posting
from ....models.skill import Skill
from ....models.salary import Salary
from ....models.job_skill import JobSkill

from ....schemas.position import PositionCreate
from ....schemas.posting import PostingCreate
from ....schemas.skill import SkillCreate
from ....schemas.salary import SalaryCreate
from ....schemas.job_skill import JobSkillCreate

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("/scrape_jobs", status_code=201)
async def create_scrape_task(role: str, base_url: str, max_pages: Optional[int], db: AsyncSession = Depends(async_get_db)):
    try:
        formatted_data = await scrape_endpoint(
            role,
            base_url,
            max_pages,
        )

        positions = [Position(**{k: v for k, v in position.items() if k != 'id'}) for position in formatted_data["Positions"]]
        postings = [Posting(**{k: v for k, v in posting.items() if k != 'id'}) for posting in formatted_data["Postings"]]
        skills = [Skill(**{k: v for k, v in skill.items() if k != 'id'}) for skill in formatted_data["Skills"]]
        salaries = [Salary(**{k: v for k, v in salary.items() if k != 'id'}) for salary in formatted_data["Salaries"]]

        existing_job_skills_result = await db.execute(
            text("SELECT posting_id, skill_id FROM job_skill")
        )
        existing_job_skills = set(existing_job_skills_result.fetchall())

        job_skills_set = set()
        job_skills = []

        for job_skill in formatted_data["JobSkills"]:
            job_skill_key = (job_skill["posting_id"], job_skill["skill_id"])
            if job_skill_key not in job_skills_set and job_skill_key not in existing_job_skills:
                job_skills_set.add(job_skill_key)
                job_skills.append(JobSkill(**{k: v for k, v in job_skill.items() if k != 'id'}))

        db.add_all(positions)
        db.add_all(postings)
        db.add_all(skills)
        db.add_all(salaries)
        db.add_all(job_skills)

        await db.commit()

        return {"message": "Data successfully inserted"}

    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
