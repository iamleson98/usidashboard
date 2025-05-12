"""add authentication station information to abnormals

Revision ID: adf1b40a3546
Revises: 40aeb61158e5
Create Date: 2025-05-12 13:02:20.313113

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'adf1b40a3546'
down_revision: Union[str, None] = '40aeb61158e5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


TABLE_NAME = "abnormals"
CheckinStationColumn = "checkin_station"
CheckoutStationColumn = "checkout_station"

def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(TABLE_NAME, sa.Column(CheckinStationColumn, sa.String(100), nullable=False))
    op.add_column(TABLE_NAME, sa.Column(CheckoutStationColumn, sa.String(100), nullable=False))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column(TABLE_NAME, CheckinStationColumn)
    op.drop_column(TABLE_NAME, CheckoutStationColumn)
