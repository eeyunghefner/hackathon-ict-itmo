from __future__ import annotations

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Room(Base):
    __tablename__ = "rooms"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    capacity: Mapped[int] = mapped_column(Integer, nullable=False)

    bookings: Mapped[list["RoomBooking"]] = relationship(back_populates="room")
    events: Mapped[list["Event"]] = relationship(back_populates="room")
