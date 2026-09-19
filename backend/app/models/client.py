from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base
from app.models.mixins import TimestampMixin, UUIDPKMixin


class Client(UUIDPKMixin, TimestampMixin, Base):
    __tablename__ = "clients"

    name: Mapped[str] = mapped_column(String(128), nullable=False)
    code: Mapped[str] = mapped_column(String(32), unique=True, nullable=False, index=True)
    contact_name: Mapped[str | None] = mapped_column(String(128), nullable=True)
    contact_email: Mapped[str | None] = mapped_column(String(255), nullable=True)
    contact_phone: Mapped[str | None] = mapped_column(String(32), nullable=True)
    status: Mapped[str] = mapped_column(String(32), default="ACTIVE", nullable=False)

    user_links: Mapped[list["ClientUser"]] = relationship(  # noqa: F821
        back_populates="client", cascade="all, delete-orphan"
    )
