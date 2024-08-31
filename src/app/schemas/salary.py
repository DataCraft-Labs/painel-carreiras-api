from datetime import datetime
from typing import Annotated, Optional
from decimal import Decimal

from pydantic import BaseModel, Field


class SalaryBase(BaseModel):
    posting_id: Annotated[int, Field(ge=1, description="Foreign key to the posting table")]
    base_salary: Annotated[
        Decimal, Field(ge=0, decimal_places=2, description="The base annual salary for the position")
    ]
    median_salary: Optional[
        Annotated[
            Decimal,
            Field(
                ge=0,
                decimal_places=2,
                description="The median annual salary, accommodating variances such as experience level",
            ),
        ]
    ]
    max_salary: Optional[
        Annotated[
            Decimal,
            Field(ge=0, decimal_places=2, description="Maximum potential salary based on performance and promotions"),
        ]
    ]
    currency: Annotated[
        str, Field(max_length=3, strict=True, description="Currency code in which the salary is paid", default="USD")
    ]


class SalaryCreate(SalaryBase):
    pass


class SalaryRead(BaseModel):
    id: Annotated[int, Field(ge=1)]
    posting_id: Annotated[int, Field(ge=1)]
    base_salary: Annotated[Decimal, Field(ge=0, decimal_places=2)]
    median_salary: Optional[Annotated[Decimal, Field(ge=0, decimal_places=2)]]
    max_salary: Optional[Annotated[Decimal, Field(ge=0, decimal_places=2)]]
    currency: Annotated[str, Field(max_length=3, strict=True)]
    created_at: datetime
    updated_at: Optional[datetime]


class SalaryUpdate(BaseModel):
    base_salary: Optional[Annotated[Decimal, Field(ge=0, decimal_places=2)]] = None
    median_salary: Optional[Annotated[Decimal, Field(ge=0, decimal_places=2)]] = None
    max_salary: Optional[Annotated[Decimal, Field(ge=0, decimal_places=2)]] = None
    currency: Optional[Annotated[str, Field(max_length=3, strict=True)]] = None
