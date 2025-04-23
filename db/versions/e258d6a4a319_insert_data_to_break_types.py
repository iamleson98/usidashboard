"""Insert data to break types

Revision ID: e258d6a4a319
Revises: 1c59bdec79ee
Create Date: 2025-04-23 14:44:33.136515

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e258d6a4a319'
down_revision: Union[str, None] = '1c59bdec79ee'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

TABLE_BREAK_TYPES = "break_types"

def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column(TABLE_BREAK_TYPES, "start_time", type_=sa.Time(), existing_type=sa.DateTime())
    op.alter_column(TABLE_BREAK_TYPES, "end_time", type_=sa.Time(), existing_type=sa.DateTime())

    op.execute("""
    INSERT INTO `break_types` (`id`, `name`, `start_time`, `end_time`, `total_time`) VALUES
    (1, 'Normal', '00:00:00', '23:59:59', 0),
    (2, 'Abnormal', '00:00:00', '23:59:59', 10),
    (3, 'Mealtime 11h20', '11:20:00', '12:20:00', 60),
    (4, 'Mealtime 11h40', '11:40:00', '12:40:00', 60),
    (5, 'Mealtime 12h', '12:00:00', '13:00:00', 60),
    (6, 'Mealtime afternoon', '17:30:00', '18:00:00', 30),
    (7, 'Offtime', '00:00:00', '23:59:59', 0);
    """)


def downgrade() -> None:
    """Downgrade schema."""
    pass
