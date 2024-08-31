from datetime import datetime
from typing import Annotated, Optional

from pydantic import BaseModel, Field


class PostingBase(BaseModel):
    position_id: Annotated[int, Field(ge=1, description="Foreign key to the position table")]
    original_title: Annotated[
        str, Field(max_length=100, description="The title of the job posting as originally listed")
    ]
    location: Annotated[str, Field(max_length=100, description="Location where the job is based")]
    company: Annotated[str, Field(max_length=100, description="Company offering the position")]
    seniority: Annotated[str, Field(max_length=50, description="Seniority level required for the position")]


class PostingCreate(PostingBase):
    pass


class PostingRead(BaseModel):
    id: Annotated[int, Field(ge=1)]
    position_id: Annotated[int, Field(ge=1)]
    original_title: Annotated[str, Field(max_length=100)]
    location: Annotated[str, Field(max_length=100)]
    company: Annotated[str, Field(max_length=100)]
    seniority: Annotated[str, Field(max_length=50)]
    created_at: datetime
    updated_at: Optional[datetime]


class PostingUpdate(BaseModel):
    position_id: Optional[Annotated[int, Field(ge=1)]] = None
    original_title: Optional[Annotated[str, Field(max_length=100)]] = None
    location: Optional[Annotated[str, Field(max_length=100)]] = None
    company: Optional[Annotated[str, Field(max_length=100)]] = None
    seniority: Optional[Annotated[str, Field(max_length=50)]] = None
