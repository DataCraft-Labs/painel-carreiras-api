from datetime import datetime, timezone
from sqlalchemy import DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from ..core.db.database import Base

class Skill(Base):
    __tablename__ = "skill"

    id: Mapped[int] = mapped_column("id", Integer, primary_key=True, autoincrement=True, nullable=False, unique=True, init=False)
    name: Mapped[str] = mapped_column("name", String, nullable=False, index=True)

    created_at: Mapped[datetime] = mapped_column("created_at", DateTime(timezone=True), default_factory=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime | None] = mapped_column("updated_at", DateTime(timezone=True), default=None)
    deleted_at: Mapped[datetime | None] = mapped_column("deleted_at", DateTime(timezone=True), default=None)
