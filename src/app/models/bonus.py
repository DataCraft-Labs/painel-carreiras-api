from datetime import datetime, timezone
from sqlalchemy import DateTime, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from ..core.db.database import Base


class Bonus(Base):
    __tablename__ = "bonus"

    id: Mapped[int] = mapped_column(
        "id", Integer, primary_key=True, autoincrement=True, nullable=False, unique=True, init=False
    )
    salary_id: Mapped[int] = mapped_column("salary_id", ForeignKey("salary.id"), nullable=False, index=True)
    type: Mapped[str] = mapped_column("type", String, nullable=False, doc="Type of bonus, e.g., Annual, Performance")
    amount: Mapped[Numeric] = mapped_column("amount", Numeric(scale=2), nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        "created_at", DateTime(timezone=True), default_factory=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime | None] = mapped_column("updated_at", DateTime(timezone=True), default=None)
