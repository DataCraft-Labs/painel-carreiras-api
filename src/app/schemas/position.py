from datetime import datetime
from typing import Annotated, Optional

from pydantic import BaseModel, Field

class PositionBase(BaseModel):
    title: Annotated[str, Field(max_length=100, description="Job title of the position")]
    description: Optional[Annotated[str, Field(description="Detailed description of the position")]]


class PositionCreate(PositionBase):
    pass


class PositionRead(BaseModel):
    id: Annotated[int, Field(ge=1)]
    title: Annotated[str, Field(max_length=100)]
    description: Optional[str]
    created_at: datetime
    updated_at: Optional[datetime]
    deleted_at: Optional[datetime]


class PositionUpdate(BaseModel):
    title: Optional[Annotated[str, Field(max_length=100)]] = None
    description: Optional[str] = None
