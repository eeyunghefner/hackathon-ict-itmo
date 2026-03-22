from __future__ import annotations

from datetime import datetime

from sqlalchemy import ForeignKey, String, TIMESTAMP, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Application(Base):
    __tablename__ = "applications"
    __table_args__ = (UniqueConstraint("team_id", "hackathon_id"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    team_id: Mapped[int] = mapped_column(
        ForeignKey("teams.id", ondelete="CASCADE"),
        nullable=False,
    )
    hackathon_id: Mapped[int] = mapped_column(
        ForeignKey("hackathons.id", ondelete="CASCADE"),
        nullable=False,
    )
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="pending")
    applied_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.utcnow)

    team: Mapped["Team"] = relationship(back_populates="applications")
    hackathon: Mapped["Hackathon"] = relationship(back_populates="applications")
