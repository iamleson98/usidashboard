"""create table break type

Revision ID: d5d5bfb16390
Revises: 1d8eb8f7abe9
Create Date: 2025-04-22 15:05:33.725505

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

TABLE_NAME = "break_types"

# revision identifiers, used by Alembic.
revision: str = 'd5d5bfb16390'
down_revision: Union[str, None] = '1d8eb8f7abe9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        TABLE_NAME,
        sa.Column('id', sa.BigInteger, primary_key=True, nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('start_time', sa.DateTime, nullable=False),
        sa.Column('end_time', sa.DateTime, nullable=False),
        sa.Column('total_time', sa.Integer, nullable=False),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table(TABLE_NAME)
