from __future__ import annotations

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class AuthorizationDetails(Base):
    __tablename__ = "authorization_details"

    id: Mapped[int] = mapped_column(primary_key=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)

    users: Mapped[list["User"]] = relationship(
        back_populates="authorization_details",
        passive_deletes=True,
    )
