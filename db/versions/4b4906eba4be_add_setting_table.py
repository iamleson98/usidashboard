"""add setting table

Revision ID: 4b4906eba4be
Revises: 7bd0045e4671
Create Date: 2025-05-14 13:35:40.244140

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4b4906eba4be'
down_revision: Union[str, None] = '7bd0045e4671'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


TABLE_NAME = "settings"

def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        TABLE_NAME,
        sa.Column("id", sa.BigInteger, primary_key=True, nullable=False, autoincrement=True),
        sa.Column("setting_type", sa.String(100), nullable=False),
        sa.Column("key", sa.String(50), nullable=False),
        sa.Column("value", sa.String(50), nullable=False),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table(TABLE_NAME)
