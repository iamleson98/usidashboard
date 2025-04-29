"""create checking event table

Revision ID: 1d8eb8f7abe9
Revises: 38c1dfd64cf4
Create Date: 2025-04-22 10:09:54.938707

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1d8eb8f7abe9'
down_revision: Union[str, None] = '38c1dfd64cf4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

TABLE_NAME = "checking_events"
EMPLOYEE_TABLE_NAME = "employees"

def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        TABLE_NAME,
        sa.Column('id', sa.BigInteger, primary_key=True, nullable=False, autoincrement=True),
        sa.Column('employee_id', sa.String(length=12), nullable=False),
        sa.Column('is_checkin', sa.Boolean, nullable=True), # if 1, check in, if 0, check out
        sa.Column('time', sa.DateTime, nullable=False),
    )

    op.create_foreign_key('fk_employee_id', TABLE_NAME, EMPLOYEE_TABLE_NAME, ['employee_id'], ['id'], ondelete="CASCADE")


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint('fk_employee_id', TABLE_NAME, type_='foreignkey')
    op.drop_table(TABLE_NAME)
