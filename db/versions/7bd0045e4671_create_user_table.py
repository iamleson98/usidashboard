"""create user table

Revision ID: 7bd0045e4671
Revises: 60124ad6d1bd
Create Date: 2025-05-13 13:47:32.384611

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from datetime import datetime

# revision identifiers, used by Alembic.
revision: str = '7bd0045e4671'
down_revision: Union[str, None] = '60124ad6d1bd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


TABLE_NAME = "users"

def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        TABLE_NAME,
        sa.Column("id", sa.BigInteger, autoincrement=True, primary_key=True, nullable=False),
        sa.Column("first_name", sa.String(100), nullable=False),
        sa.Column("last_name", sa.String(100), nullable=False),
        sa.Column("email", sa.String(200), nullable=False),
        sa.Column("password", sa.String(256), nullable=False),
        sa.Column("created_at", sa.DateTime, nullable=False, default=datetime.now),
        sa.Column("ipdated_at", sa.DateTime, nullable=True, default=datetime.now),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table(TABLE_NAME)
