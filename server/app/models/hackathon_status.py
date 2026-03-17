from __future__ import annotations

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class HackathonStatus(Base):
    __tablename__ = "hackathon_status"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)

    hackathons: Mapped[list["Hackathon"]] = relationship(back_populates="status")
