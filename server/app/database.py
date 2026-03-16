from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
import os
from dotenv import load_dotenv
from datetime import datetime
from sqlalchemy import (
    String,
    Text,
    Integer,
    ForeignKey,
    TIMESTAMP,
    CheckConstraint,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_async_engine(DATABASE_URL, echo=True)

AsyncSessionLocal = async_sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)

Base = declarative_base()


async def get_async_session():
    async with AsyncSessionLocal() as session:
        yield session

class Role(Base):
    tablename = "roles"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)

    users: Mapped[list["User"]] = relationship(back_populates="role")


class AuthorizationDetails(Base):
    tablename = "authorization_details"

    id: Mapped[int] = mapped_column(primary_key=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)

    users: Mapped[list["User"]] = relationship(back_populates="authorization_details")


class HackathonStatus(Base):
    tablename = "hackathon_status"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)

    hackathons: Mapped[list["Hackathon"]] = relationship(back_populates="status")


class User(Base):
    tablename = "users"

    id: Mapped[int] = mapped_column(primary_key=True)

    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    phone: Mapped[str | None] = mapped_column(String(20))

    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id", ondelete="RESTRICT"))
    authorization_details_id: Mapped[int] = mapped_column(
        ForeignKey("authorization_details.id", ondelete="CASCADE")
    )

    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP, default=datetime.utcnow
    )
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP, default=datetime.utcnow
    )

    role: Mapped["Role"] = relationship(back_populates="users")
    authorization_details: Mapped["AuthorizationDetails"] = relationship(
        back_populates="users"
    )

    applications: Mapped[list["Application"]] = relationship(back_populates="user")
    teams: Mapped[list["TeamMember"]] = relationship(back_populates="user")
    captain_teams: Mapped[list["Team"]] = relationship(back_populates="captain")


class Hackathon(Base):
    tablename = "hackathons"

    id: Mapped[int] = mapped_column(primary_key=True)

    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)

    status_id: Mapped[int | None] = mapped_column(
        ForeignKey("hackathon_status.id", ondelete="SET NULL")
    )

    registration_start_date: Mapped[datetime] = mapped_column(TIMESTAMP, nullable=False)
    registration_end_date: Mapped[datetime] = mapped_column(TIMESTAMP, nullable=False)
    start_date: Mapped[datetime] = mapped_column(TIMESTAMP, nullable=False)
    end_date: Mapped[datetime] = mapped_column(TIMESTAMP, nullable=False)

    max_participants: Mapped[int | None] = mapped_column(
        Integer, CheckConstraint("max_participants > 0")
    )
    max_teams: Mapped[int | None] = mapped_column(
        Integer, CheckConstraint("max_teams > 0")
    )
    max_team_size: Mapped[int] = mapped_column(default=5)

    created_by: Mapped[int | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL")
    )

    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP, default=datetime.utcnow
    )
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP, default=datetime.utcnow
    )

    status: Mapped["HackathonStatus"] = relationship(back_populates="hackathons")
    applications: Mapped[list["Application"]] = relationship(back_populates="hackathon")
    teams: Mapped[list["Team"]] = relationship(back_populates="hackathon")


class Application(Base):
    tablename = "applications"

    table_args = (
        UniqueConstraint("user_id", "hackathon_id"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    hackathon_id: Mapped[int] = mapped_column(
        ForeignKey("hackathons.id", ondelete="CASCADE"), nullable=False
    )

    applied_at: Mapped[datetime] = mapped_column(
        TIMESTAMP, default=datetime.utcnow
    )

    user: Mapped["User"] = relationship(back_populates="applications")
    hackathon: Mapped["Hackathon"] = relationship(back_populates="applications")


class Team(Base):
    tablename = "teams"

    table_args = (
        UniqueConstraint("name", "hackathon_id"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(String(255), nullable=False)

    hackathon_id: Mapped[int] = mapped_column(
        ForeignKey("hackathons.id", ondelete="CASCADE"), nullable=False
    )

    captain_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL")
    )

    max_members: Mapped[int | None] = mapped_column(Integer)

    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP, default=datetime.utcnow
    )

    hackathon: Mapped["Hackathon"] = relationship(back_populates="teams")
    captain: Mapped["User"] = relationship(back_populates="captain_teams")

    members: Mapped[list["TeamMember"]] = relationship(back_populates="team")


class TeamMember(Base):
    tablename = "team_members"

    team_id: Mapped[int] = mapped_column(
        ForeignKey("teams.id", ondelete="CASCADE"), primary_key=True
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    )

    joined_at: Mapped[datetime] = mapped_column(
        TIMESTAMP, default=datetime.utcnow
    )

    team: Mapped["Team"] = relationship(back_populates="members")
    user: Mapped["User"] = relationship(back_populates="teams")
        