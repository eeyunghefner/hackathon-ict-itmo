from __future__ import annotations

from datetime import datetime

from sqlalchemy import ForeignKey, TIMESTAMP, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Application(Base):
    __tablename__ = "applications"
    __table_args__ = (UniqueConstraint("user_id", "hackathon_id"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )
    hackathon_id: Mapped[int] = mapped_column(
        ForeignKey("hackathons.id", ondelete="CASCADE"),
        nullable=False,
    )
    applied_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.utcnow)

    user: Mapped["User"] = relationship(back_populates="applications")
    hackathon: Mapped["Hackathon"] = relationship(back_populates="applications")
