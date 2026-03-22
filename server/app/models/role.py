from __future__ import annotations

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Role(Base):
    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)

    users_association: Mapped[list["User"]] = relationship(
        secondary="user_role",
        back_populates="roles_association",
        passive_deletes=True,
    )
