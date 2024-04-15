from datetime import datetime
from typing import Annotated, Optional
from pydantic import BaseModel, Field

class BonusBase(BaseModel):
    type: Annotated[str, Field(max_length=50, description="Type of bonus, e.g., Annual, Performance")]
    amount: Annotated[float, Field(ge=0, description="Amount of the bonus")]


class BonusCreate(BonusBase):
    salary_id: Annotated[int, Field(ge=1, description="Foreign key to the salary table")]


class BonusRead(BaseModel):
    id: Annotated[int, Field(ge=1)]
    salary_id: Annotated[int, Field(ge=1)]
    type: Annotated[str, Field(max_length=50)]
    amount: Annotated[float, Field(ge=0)]
    created_at: datetime
    updated_at: Optional[datetime]


class BonusUpdate(BaseModel):
    type: Optional[Annotated[str, Field(max_length=50)]] = None
    amount: Optional[Annotated[float, Field(ge=0)]] = None
