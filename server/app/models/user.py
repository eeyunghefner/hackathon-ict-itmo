from __future__ import annotations

from datetime import datetime

from sqlalchemy import ForeignKey, String, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    university: Mapped[str | None] = mapped_column(String(255))
    phone: Mapped[str | None] = mapped_column(String(20))
    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id", ondelete="RESTRICT"))
    authorization_details_id: Mapped[int] = mapped_column(
        ForeignKey("authorization_details.id", ondelete="CASCADE")
    )
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    role: Mapped["Role"] = relationship(back_populates="users")
    authorization_details: Mapped["AuthorizationDetails"] = relationship(
        back_populates="users"
    )
    teams: Mapped[list["TeamMember"]] = relationship(back_populates="user")
    captain_teams: Mapped[list["Team"]] = relationship(
        back_populates="captain",
        foreign_keys="Team.captain_id",
    )
