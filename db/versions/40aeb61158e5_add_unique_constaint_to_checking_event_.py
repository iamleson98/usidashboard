"""add unique constaint to checking event table

Revision ID: 40aeb61158e5
Revises: 240002b9a94d
Create Date: 2025-05-05 10:28:23.432135

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '40aeb61158e5'
down_revision: Union[str, None] = '240002b9a94d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

constraint_name = "checking_events_unique_employee_check_type_time_key"
TABLE_NAME = "checking_events"
UNIQUE_COLS = ["employee_id", "is_checkin", "time"]

def upgrade() -> None:
    """Upgrade schema."""
    op.create_unique_constraint(constraint_name, TABLE_NAME, UNIQUE_COLS)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint(constraint_name, TABLE_NAME, type_="unique")
