from __future__ import annotations

from datetime import datetime

from sqlalchemy import ForeignKey, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class RoomBooking(Base):
    __tablename__ = "room_bookings"

    id: Mapped[int] = mapped_column(primary_key=True)
    room_id: Mapped[int] = mapped_column(
        ForeignKey("rooms.id", ondelete="CASCADE"),
        nullable=False,
    )
    created_by: Mapped[int | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL")
    )
    start_time: Mapped[datetime] = mapped_column(TIMESTAMP, nullable=False)
    end_time: Mapped[datetime] = mapped_column(TIMESTAMP, nullable=False)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.utcnow)

    room: Mapped["Room"] = relationship(back_populates="bookings")
