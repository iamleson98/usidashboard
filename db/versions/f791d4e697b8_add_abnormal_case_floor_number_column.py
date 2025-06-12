"""add abnormal case floor number column

Revision ID: f791d4e697b8
Revises: 36603c106e0c
Create Date: 2025-06-12 14:37:16.856046

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f791d4e697b8'
down_revision: Union[str, None] = '36603c106e0c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

TABLE_NAME = "abnormals"


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(TABLE_NAME, sa.Column("floor", sa.SmallInteger, nullable=False))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column(TABLE_NAME, "floor")
