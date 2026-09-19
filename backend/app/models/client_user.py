import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base
from app.models.mixins import UUIDPKMixin


class ClientUser(UUIDPKMixin, Base):
    __tablename__ = "client_users"
    __table_args__ = (UniqueConstraint("client_id", "user_id", name="uq_client_user"),)

    client_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("clients.id", ondelete="CASCADE"), nullable=False, index=True
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    client: Mapped["Client"] = relationship(back_populates="user_links")  # noqa: F821
    user: Mapped["User"] = relationship(back_populates="client_links")  # noqa: F821
