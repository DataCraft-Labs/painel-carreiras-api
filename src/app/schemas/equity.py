from datetime import datetime
from typing import Annotated, Optional

from pydantic import BaseModel, Field


class EquityBase(BaseModel):
    type: Annotated[str, Field(max_length=50, description="Type of equity, e.g., Stock Options, RSUs")]
    amount: Annotated[float, Field(ge=0, description="Amount of the equity")]
    vesting_period: Annotated[str, Field(max_length=50, description="Vesting period, e.g., 4 years")]


class EquityCreate(EquityBase):
    salary_id: Annotated[int, Field(ge=1, description="Foreign key to the salary table")]


class EquityRead(BaseModel):
    id: Annotated[int, Field(ge=1)]
    salary_id: Annotated[int, Field(ge=1)]
    type: Annotated[str, Field(max_length=50)]
    amount: Annotated[float, Field(ge=0)]
    vesting_period: Annotated[str, Field(max_length=50)]
    created_at: str
    updated_at: Optional[str]


class EquityUpdate(BaseModel):
    type: Optional[Annotated[str, Field(max_length=50)]] = None
    amount: Optional[Annotated[float, Field(ge=0)]] = None
    vesting_period: Optional[Annotated[str, Field(max_length=50)]] = None
