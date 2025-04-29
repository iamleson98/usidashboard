"""Add abnormal table

Revision ID: 240002b9a94d
Revises: 16213713d251
Create Date: 2025-04-29 15:03:31.133175

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '240002b9a94d'
down_revision: Union[str, None] = '16213713d251'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


TABLE_NAME = "abnormals"
EMPLOYEE_TABLE_NAME = "employees"


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        TABLE_NAME,
        sa.Column("id", sa.BigInteger, primary_key=True, autoincrement=True),
        sa.Column("employee_id", sa.String(20), nullable=False),
        sa.Column("out_time", sa.DateTime, nullable=False),
        sa.Column("in_time", sa.DateTime, nullable=False),
        sa.Column("total_mins", sa.Integer, nullable=False),
    )

    op.create_foreign_key("fk_abnormals_employee_id", TABLE_NAME, EMPLOYEE_TABLE_NAME, ["employee_id"], ["id"], ondelete="CASCADE")
    op.create_unique_constraint("abnormals_unique_together_key", TABLE_NAME, ["employee_id", "out_time", "in_time"])

def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint('fk_abnormals_employee_id', TABLE_NAME, type_='foreignkey')
    op.drop_constraint('abnormals_unique_together_key', TABLE_NAME, type_='unique')
    op.drop_table(TABLE_NAME)
