"""add short department to employee table

Revision ID: fe322aa448b3
Revises: 4b4906eba4be
Create Date: 2025-05-24 15:16:07.854621

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fe322aa448b3'
down_revision: Union[str, None] = '4b4906eba4be'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

tableName = "employees"
columnName = "short_dept"

def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        tableName,
        sa.Column(columnName, sa.String(length=20))
    )

def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column(tableName, columnName)
