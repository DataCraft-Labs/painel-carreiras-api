from datetime import datetime, timezone
from sqlalchemy import DateTime, ForeignKey, Index, Integer
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.schema import UniqueConstraint

from ..core.db.database import Base

class JobSkill(Base):
    __tablename__ = "job_skill"
    
    id: Mapped[int] = mapped_column("id", Integer, primary_key=True, autoincrement=True, nullable=False, unique=True, init=False)
    posting_id: Mapped[int] = mapped_column("posting_id", ForeignKey("posting.id"), nullable=False, index=True)
    skill_id: Mapped[int] = mapped_column("skill_id", ForeignKey("skill.id"), nullable=False, index=True)

    created_at: Mapped[datetime] = mapped_column("created_at", DateTime(timezone=True), default_factory=lambda: datetime.now(timezone.utc))
    
    __table_args__ = (
        UniqueConstraint('posting_id', 'skill_id', name='uix_posting_id_skill_id'),
        Index('ix_jobskills_posting_skill', posting_id, skill_id, unique=True),
    )
