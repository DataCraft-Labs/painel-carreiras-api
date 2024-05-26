import asyncio
import logging
import random
from decimal import Decimal
from datetime import datetime, timezone, timedelta

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select

from ..app.core.db.database import Base, DATABASE_URL
from ..app.models.benefit import Benefit
from ..app.models.bonus import Bonus
from ..app.models.equity import Equity
from ..app.models.job_skill import JobSkill
from ..app.models.position import Position
from ..app.models.posting import Posting
from ..app.models.rate_limit import RateLimit
from ..app.models.salary import Salary
from ..app.models.skill import Skill

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async_engine = create_async_engine(DATABASE_URL, echo=False, future=True)

local_session = sessionmaker(bind=async_engine, class_=AsyncSession, expire_on_commit=False)

async def create_tables():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("All tables created successfully.")

async def add_positions(session: AsyncSession):
    positions = [
        Position(title="Software Engineer", description="Develops software solutions."),
        Position(title="Data Scientist", description="Analyzes data for insights."),
        Position(title="Project Manager", description="Oversees project progress."),
        Position(title="DevOps Engineer", description="Manages infrastructure and CI/CD."),
        Position(title="QA Engineer", description="Ensures software quality."),
        Position(title="Product Manager", description="Defines product requirements."),
        Position(title="UX Designer", description="Designs user interfaces."),
        Position(title="System Analyst", description="Analyzes system requirements."),
        Position(title="Database Administrator", description="Manages databases."),
        Position(title="Network Engineer", description="Maintains network systems."),
        Position(title="Security Engineer", description="Ensures system security."),
    ]
    session.add_all(positions)
    await session.commit()
    logger.info("Positions added successfully.")

async def add_postings(session: AsyncSession):
    result = await session.execute(select(Position.id))
    position_ids = [row[0] for row in result.fetchall()]

    locations = ["San Francisco", "New York", "Chicago", "Austin", "Seattle", "Boston", "Los Angeles", "Denver", "Portland", "San Diego", "Miami"]
    companies = ["TechCorp", "WebWorks", "Innovatech", "CodeBase", "TechWorld", "AppWorks", "FunTech", "CloudNine", "EmbedTech", "AIBrain", "BlockChainCo"]
    seniorities = ["Junior", "Mid", "Senior"]

    postings = []
    for position_id in position_ids:
        postings.extend([
            Posting(position_id=position_id, original_title=f"{random.choice(companies)} {i+1}", location=random.choice(locations), company=random.choice(companies), seniority=random.choice(seniorities))
            for i in range(10)
        ])
    session.add_all(postings)
    await session.commit()
    logger.info("Postings added successfully.")

async def add_salaries(session: AsyncSession):
    result = await session.execute(select(Posting.id))
    posting_ids = [row[0] for row in result.fetchall()]

    num_salaries = len(posting_ids) * 10
    base_salaries = [int(random.gauss(115000, 15000)) for _ in range(num_salaries * 3)]

    salaries = [
        Salary(posting_id=posting_id, base_salary=Decimal(base_salaries.pop()), median_salary=Decimal(base_salaries.pop()), max_salary=Decimal(base_salaries.pop()), currency='USD')
        for posting_id in posting_ids
        for _ in range(10)
    ]
    session.add_all(salaries)
    await session.commit()
    logger.info("Salaries added successfully.")

async def add_benefits(session: AsyncSession):
    result = await session.execute(select(Salary.id))
    salary_ids = [row[0] for row in result.fetchall()]

    benefit_types = ["Health Insurance", "Retirement Plan", "Paid Time Off", "Life Insurance", "Stock Options", "Dental Insurance", "Vision Insurance", "Flexible Hours", "Work from Home", "Gym Membership", "Commuter Benefits"]
    descriptions = [
        "Full health coverage.", "401k matching.", "20 days per year.", "Coverage for life insurance.", "Equity in the company.",
        "Full dental coverage.", "Full vision coverage.", "Flexible working hours.", "Option to work remotely.", "Free gym membership.", "Subsidized commuting costs."
    ]

    benefits = [
        Benefit(salary_id=salary_id, benefit_type=benefit_types[i % len(benefit_types)], description=descriptions[i % len(descriptions)])
        for salary_id in salary_ids
        for i in range(10)
    ]
    session.add_all(benefits)
    await session.commit()
    logger.info("Benefits added successfully.")

async def add_bonuses(session: AsyncSession):
    result = await session.execute(select(Salary.id))
    salary_ids = [row[0] for row in result.fetchall()]

    bonus_types = ["Annual", "Performance", "Signing", "Referral", "Retention", "Holiday", "Project", "Profit Sharing", "Sales", "Commission", "Incentive"]

    bonuses = [
        Bonus(salary_id=salary_id, type=bonus_types[i % len(bonus_types)], amount=Decimal(random.randint(1000, 10000)))
        for salary_id in salary_ids
        for i in range(10)
    ]
    session.add_all(bonuses)
    await session.commit()
    logger.info("Bonuses added successfully.")

async def add_equities(session: AsyncSession):
    result = await session.execute(select(Salary.id))
    salary_ids = [row[0] for row in result.fetchall()]

    equity_types = ["Stock Options", "RSUs", "ESPP", "Performance Shares", "Stock Grants", "Phantom Shares", "SARs", "Warrants", "Convertible Notes", "Growth Shares", "Profit Interests"]
    vesting_periods = ["2 years", "3 years", "4 years", "5 years", "6 years"]

    equities = [
        Equity(salary_id=salary_id, type=equity_types[i % len(equity_types)], amount=Decimal(random.randint(5000, 20000)), vesting_period=random.choice(vesting_periods))
        for salary_id in salary_ids
        for i in range(10)
    ]
    session.add_all(equities)
    await session.commit()
    logger.info("Equities added successfully.")

async def add_skills(session: AsyncSession):
    skill_names = ["Python", "Machine Learning", "Data Analysis", "Project Management", "DevOps", "Software Testing", "Product Management", "User Experience Design", "Systems Analysis", "Database Management", "Network Security", "Cybersecurity", "Cloud Computing", "Artificial Intelligence", "Blockchain Technology"]

    skills = [
        Skill(name=skill_names[i % len(skill_names)])
        for i in range(15)
    ]
    session.add_all(skills)
    await session.commit()
    logger.info("Skills added successfully.")

async def add_job_skills(session: AsyncSession):
    result_posting = await session.execute(select(Posting.id))
    posting_ids = [row[0] for row in result_posting.fetchall()]

    result_skill = await session.execute(select(Skill.id))
    skill_ids = [row[0] for row in result_skill.fetchall()]

    job_skills = []

    for posting_id in posting_ids:
        chosen_skills = set()
        while len(chosen_skills) < 10:
            skill_id = random.choice(skill_ids)
            if skill_id not in chosen_skills:
                chosen_skills.add(skill_id)
                job_skills.append(JobSkill(posting_id=posting_id, skill_id=skill_id))

    session.add_all(job_skills)
    await session.commit()
    logger.info("Job skills added successfully.")

async def main():
    async with local_session() as session:
        await create_tables()
        await add_positions(session)
        await add_postings(session)
        await add_salaries(session)
        await add_benefits(session)
        await add_bonuses(session)
        await add_equities(session)
        await add_skills(session)
        await add_job_skills(session)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
