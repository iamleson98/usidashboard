"""create table break

Revision ID: 1c59bdec79ee
Revises: d5d5bfb16390
Create Date: 2025-04-22 15:48:22.819084

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '1c59bdec79ee'
down_revision: Union[str, None] = 'd5d5bfb16390'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

TABLE_NAME = "breaks"
BREAK_TYPE_TABLE_NAME = "break_types"
EMPLOYEE_TABLE_NAME = "employees"

def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        TABLE_NAME,
        sa.Column('id', sa.BigInteger, autoincrement=True, primary_key=True, nullable=False),
        sa.Column('employee_id', sa.String(12), nullable=False),
        sa.Column('in_time', sa.DateTime, nullable=True),
        sa.Column('out_time', sa.DateTime, nullable=True),
        sa.Column('minutes', sa.Integer, nullable=False),
        sa.Column('break_type_id', sa.BigInteger, nullable=False),
    )

    op.create_foreign_key('fk_break_type_id', TABLE_NAME, BREAK_TYPE_TABLE_NAME, ['break_type_id'], ['id'])
    op.create_foreign_key('fk_breaks_employee_id', TABLE_NAME, EMPLOYEE_TABLE_NAME, ['employee_id'], ['id'], ondelete="CASCADE")

def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint('fk_break_type_id', TABLE_NAME, type_='foreignkey')
    op.drop_constraint('fk_breaks_employee_id', TABLE_NAME, type_='foreignkey')

    op.drop_table(TABLE_NAME)
