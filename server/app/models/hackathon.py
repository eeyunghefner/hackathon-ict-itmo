from __future__ import annotations

from datetime import datetime

from sqlalchemy import CheckConstraint, ForeignKey, Integer, String, TIMESTAMP, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Hackathon(Base):
    __tablename__ = "hackathons"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    theme: Mapped[str] = mapped_column(String(255), nullable=False)
    event_format: Mapped[str] = mapped_column("format", String(50), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    rules: Mapped[str | None] = mapped_column(Text)
    status_id: Mapped[int | None] = mapped_column(
        ForeignKey("hackathon_status.id", ondelete="SET NULL")
    )
    registration_start_date: Mapped[datetime] = mapped_column(TIMESTAMP, nullable=False)
    registration_end_date: Mapped[datetime] = mapped_column(TIMESTAMP, nullable=False)
    start_date: Mapped[datetime] = mapped_column(TIMESTAMP, nullable=False)
    end_date: Mapped[datetime] = mapped_column(TIMESTAMP, nullable=False)
    max_participants: Mapped[int | None] = mapped_column(
        Integer,
        CheckConstraint("max_participants > 0"),
    )
    max_teams: Mapped[int | None] = mapped_column(
        Integer,
        CheckConstraint("max_teams > 0"),
    )
    max_team_size: Mapped[int] = mapped_column(default=5)
    created_by: Mapped[int | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL")
    )
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    status: Mapped["HackathonStatus"] = relationship(back_populates="hackathons")
    applications: Mapped[list["Application"]] = relationship(back_populates="hackathon")
    events: Mapped[list["Event"]] = relationship(back_populates="hackathon")
    teams: Mapped[list["Team"]] = relationship(back_populates="hackathon")
