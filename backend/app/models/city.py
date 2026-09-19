from datetime import datetime

from sqlalchemy import DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.session import Base
from app.models.mixins import UUIDPKMixin


class City(UUIDPKMixin, Base):
    __tablename__ = "cities"

    name: Mapped[str] = mapped_column(String(128), nullable=False)
    state: Mapped[str | None] = mapped_column(String(128), nullable=True)
    country: Mapped[str] = mapped_column(String(128), default="India", nullable=False)
    status: Mapped[str] = mapped_column(String(32), default="ACTIVE", nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
