from __future__ import annotations

from datetime import datetime

from sqlalchemy import ForeignKey, Integer, String, TIMESTAMP, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Team(Base):
    __tablename__ = "teams"
    __table_args__ = (UniqueConstraint("name", "hackathon_id"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    hackathon_id: Mapped[int] = mapped_column(
        ForeignKey("hackathons.id", ondelete="CASCADE"),
        nullable=False,
    )
    captain_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL")
    )
    max_members: Mapped[int | None] = mapped_column(Integer)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.utcnow)

    hackathon: Mapped["Hackathon"] = relationship(back_populates="teams")
    captain: Mapped["User"] = relationship(
        back_populates="captain_teams",
        foreign_keys=[captain_id],
    )
    members: Mapped[list["TeamMember"]] = relationship(back_populates="team")
