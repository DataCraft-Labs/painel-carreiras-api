from datetime import datetime, timezone
from sqlalchemy import DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from ..core.db.database import Base


class Posting(Base):
    __tablename__ = "posting"

    id: Mapped[int] = mapped_column(
        "id", Integer, primary_key=True, autoincrement=True, nullable=False, unique=True, init=False
    )
    position_id: Mapped[int] = mapped_column("position_id", ForeignKey("position.id"), nullable=False, index=True)
    original_title: Mapped[str] = mapped_column("original_title", String, nullable=False)
    location: Mapped[str] = mapped_column("location", String, nullable=False, index=True)
    company: Mapped[str] = mapped_column("company", String, nullable=False, index=True)
    seniority: Mapped[str] = mapped_column("seniority", String, nullable=False, index=True)

    created_at: Mapped[datetime] = mapped_column(
        "created_at", DateTime(timezone=True), default_factory=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime | None] = mapped_column("updated_at", DateTime(timezone=True), default=None)
