from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, Field

class JobSkillBase(BaseModel):
    posting_id: Annotated[int, Field(ge=1, description="Foreign key to the posting table")]
    skill_id: Annotated[int, Field(ge=1, description="Foreign key to the skill table")]


class JobSkillCreate(JobSkillBase):
    pass


class JobSkillRead(BaseModel):
    id: Annotated[int, Field(ge=1)]
    posting_id: Annotated[int, Field(ge=1)]
    skill_id: Annotated[int, Field(ge=1)]
    created_at: datetime


class JobSkillUpdate(BaseModel):
    pass
