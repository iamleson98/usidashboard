"""add station column to checking event table

Revision ID: 60124ad6d1bd
Revises: adf1b40a3546
Create Date: 2025-05-12 14:17:34.767822

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '60124ad6d1bd'
down_revision: Union[str, None] = 'adf1b40a3546'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


TABLE = "checking_events"
COLUMN = "station"

def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(TABLE, sa.Column(COLUMN, sa.String(100), nullable=False))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column(TABLE, COLUMN)
