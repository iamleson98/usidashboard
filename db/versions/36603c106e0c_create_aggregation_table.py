"""create aggregation table

Revision ID: 36603c106e0c
Revises: fe322aa448b3
Create Date: 2025-06-06 16:10:57.573322

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from datetime import datetime


# revision identifiers, used by Alembic.
revision: str = '36603c106e0c'
down_revision: Union[str, None] = 'fe322aa448b3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

TABLE_NAME = "aggregations"
default_attendance = r"'{}'"

def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        TABLE_NAME,
        sa.Column("id", sa.BigInteger, primary_key=True, autoincrement=True, nullable=False),
        sa.Column("updated_at", sa.DateTime, nullable=False, default=datetime.now),
        sa.Column("live_attendances", sa.JSON),
    )

    op.execute(r"INSERT INTO aggregations (live_attendances, updated_at) VALUES ('{}', NOW())")


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table(TABLE_NAME)
