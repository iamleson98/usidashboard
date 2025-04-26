"""test

Revision ID: 8b508513d5e2
Revises: e258d6a4a319
Create Date: 2025-04-26 09:46:21.906438

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8b508513d5e2'
down_revision: Union[str, None] = 'e258d6a4a319'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
