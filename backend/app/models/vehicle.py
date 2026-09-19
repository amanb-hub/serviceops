import uuid

from sqlalchemy import ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base
from app.models.mixins import TimestampMixin, UUIDPKMixin


class Vehicle(UUIDPKMixin, TimestampMixin, Base):
    __tablename__ = "vehicles"

    registration_number: Mapped[str] = mapped_column(
        String(32), unique=True, nullable=False, index=True
    )
    client_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("clients.id", ondelete="SET NULL"), nullable=True, index=True
    )
    city_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("cities.id", ondelete="SET NULL"), nullable=True, index=True
    )
    make: Mapped[str | None] = mapped_column(String(64), nullable=True)
    model: Mapped[str | None] = mapped_column(String(64), nullable=True)
    vehicle_type: Mapped[str | None] = mapped_column(String(32), nullable=True)  # e.g. 2W, 3W, 4W
    status: Mapped[str] = mapped_column(String(32), default="ACTIVE", nullable=False)
    # ACTIVE, IN_SERVICE, OFF_ROAD, DECOMMISSIONED

    client: Mapped["Client | None"] = relationship()  # noqa: F821
    city: Mapped["City | None"] = relationship()  # noqa: F821
