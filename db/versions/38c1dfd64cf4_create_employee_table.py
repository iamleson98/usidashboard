"""create employee table

Revision ID: 38c1dfd64cf4
Revises: 
Create Date: 2025-04-22 09:49:29.763815

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '38c1dfd64cf4'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

TABLE_NAME = "employees"

def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        TABLE_NAME,
        sa.Column('id', sa.String(length=12), nullable=False),
        sa.Column('first_name', sa.String(length=255), nullable=False),
        sa.Column('last_name', sa.String(length=255), nullable=False),
        sa.Column('card_no', sa.String(length=20), nullable=False),
        sa.Column('is_visitor', sa.Boolean(), nullable=False, default=False),
        sa.Column('department', sa.String(length=500), nullable=False),
        sa.PrimaryKeyConstraint('id'),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table(TABLE_NAME)
