from datetime import datetime, timezone
from decimal import Decimal

from sqlalchemy import DateTime, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from ..core.db.database import Base

class Salary(Base):
    __tablename__ = "salary"

    id: Mapped[int] = mapped_column("id", Integer, primary_key=True, autoincrement=True, nullable=False, unique=True, init=False)
    posting_id: Mapped[int] = mapped_column("posting_id", ForeignKey("posting.id"), nullable=False, index=True)
    base_salary: Mapped[Decimal] = mapped_column("base_salary", Numeric(scale=2), nullable=False)
    median_salary: Mapped[Decimal] = mapped_column("median_salary", Numeric(scale=2), nullable=True)
    max_salary: Mapped[Decimal] = mapped_column("max_salary", Numeric(scale=2), nullable=True, doc='Maximum potential salary based on performance and promotions')
    currency: Mapped[str] = mapped_column("currency", String(length=3), default='USD', doc='Currency in which the salary and compensation are paid')

    created_at: Mapped[datetime] = mapped_column("created_at", DateTime(timezone=True), default_factory=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime | None] = mapped_column("updated_at", DateTime(timezone=True), default=None)
