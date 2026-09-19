import uuid
from datetime import datetime

from sqlalchemy import DateTime, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base
from app.models.mixins import UUIDPKMixin


class Role(UUIDPKMixin, Base):
    __tablename__ = "roles"

    name: Mapped[str] = mapped_column(String(64), unique=True, nullable=False, index=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    users: Mapped[list["User"]] = relationship(back_populates="role")  # noqa: F821


# Canonical role names. Seed script uses these; app code should reference
# this enum rather than hard-coding role strings.
class RoleName:
    SUPER_ADMIN = "SUPER_ADMIN"
    OPERATIONS_MANAGER = "OPERATIONS_MANAGER"
    CITY_MANAGER = "CITY_MANAGER"
    SERVICE_COORDINATOR = "SERVICE_COORDINATOR"
    TECHNICIAN = "TECHNICIAN"
    CLIENT_USER = "CLIENT_USER"
    FINANCE_ADMIN = "FINANCE_ADMIN"

    ALL = [
        SUPER_ADMIN,
        OPERATIONS_MANAGER,
        CITY_MANAGER,
        SERVICE_COORDINATOR,
        TECHNICIAN,
        CLIENT_USER,
        FINANCE_ADMIN,
    ]
