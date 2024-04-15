from datetime import datetime
from typing import Annotated, Optional

from pydantic import BaseModel, Field

class SkillBase(BaseModel):
    name: Annotated[str, Field(min_length=1, max_length=100, strip_whitespace=True, description="Name of the skill")]


class SkillCreate(SkillBase):
    pass


class SkillRead(BaseModel):
    id: Annotated[int, Field(ge=1)]
    name: Annotated[str, Field(min_length=1, max_length=100, strip_whitespace=True)]
    created_at: datetime
    updated_at: Optional[datetime]
    deleted_at: Optional[datetime]


class SkillUpdate(BaseModel):
    name: Optional[Annotated[str, Field(min_length=1, max_length=100, strip_whitespace=True)]] = None
