from datetime import datetime
from typing import Annotated, Optional
from pydantic import BaseModel, Field

class BenefitsBase(BaseModel):
    benefit_type: Annotated[str, Field(max_length=100)]
    description: Optional[Annotated[str, Field(max_length=500)]]


class BenefitsCreate(BenefitsBase):
    salary_id: Annotated[int, Field(ge=1)]


class BenefitsRead(BaseModel):
    id: Annotated[int, Field(ge=1)]
    salary_id: Annotated[int, Field(ge=1)]
    benefit_type: Annotated[str, Field(max_length=100)]
    description: Optional[Annotated[str, Field(max_length=500)]]
    created_at: datetime
    updated_at: Optional[datetime]


class BenefitsUpdate(BaseModel):
    benefit_type: Optional[Annotated[str, Field(max_length=100)]] = None
    description: Optional[Annotated[str, Field(max_length=500)]] = None
