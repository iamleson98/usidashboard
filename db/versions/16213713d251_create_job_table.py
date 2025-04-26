"""create job table

Revision ID: 16213713d251
Revises: 8b508513d5e2
Create Date: 2025-04-26 12:53:14.622759

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from datetime import datetime


# revision identifiers, used by Alembic.
revision: str = '16213713d251'
down_revision: Union[str, None] = '8b508513d5e2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

JOB_TABLES = "jobs"

def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        JOB_TABLES,
        sa.Column("id", sa.BigInteger, autoincrement=True, primary_key=True, nullable=False),
        sa.Column('job_type', sa.String(100), nullable=False),
        sa.Column('execution_at', sa.DateTime, default=datetime),
        sa.Column('status', sa.Boolean, nullable=False),
        sa.Column('reason', sa.String(1000), nullable=True),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table(JOB_TABLES)
