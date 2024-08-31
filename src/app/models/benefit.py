from datetime import datetime, timezone
from sqlalchemy import DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from ..core.db.database import Base


class Benefit(Base):
    __tablename__ = "benefit"

    id: Mapped[int] = mapped_column(
        "id", Integer, primary_key=True, autoincrement=True, nullable=False, unique=True, init=False
    )
    salary_id: Mapped[int] = mapped_column("salary_id", ForeignKey("salary.id"), nullable=False, index=True)
    benefit_type: Mapped[str] = mapped_column("benefit_type", String, nullable=False)
    description: Mapped[str] = mapped_column("description", String, nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        "created_at", DateTime(timezone=True), default_factory=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime | None] = mapped_column("updated_at", DateTime(timezone=True), default=None)
