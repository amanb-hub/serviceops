"""add vehicles table

Revision ID: 0002
Revises: 0001
Create Date: 2026-09-20

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision = "0002"
down_revision = "0001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "vehicles",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("registration_number", sa.String(32), nullable=False, unique=True),
        sa.Column("client_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("clients.id", ondelete="SET NULL"), nullable=True),
        sa.Column("city_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("cities.id", ondelete="SET NULL"), nullable=True),
        sa.Column("make", sa.String(64), nullable=True),
        sa.Column("model", sa.String(64), nullable=True),
        sa.Column("vehicle_type", sa.String(32), nullable=True),
        sa.Column("status", sa.String(32), nullable=False, server_default="ACTIVE"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("ix_vehicles_registration_number", "vehicles", ["registration_number"])
    op.create_index("ix_vehicles_client_id", "vehicles", ["client_id"])
    op.create_index("ix_vehicles_city_id", "vehicles", ["city_id"])


def downgrade() -> None:
    op.drop_table("vehicles")
