from models.base import EntityMeta
import sqlalchemy as sq
from sqlalchemy.orm import relationship

class BreakType(EntityMeta):
    __tablename__ = "break_types"

    id = sq.Column(sq.String(length=12), nullable=False, primary_key=True)
    name = sq.Column(sq.String(length=255), nullable=False)
    start_time = sq.Column(sq.DateTime, nullable=False)
    end_time = sq.Column(sq.DateTime, nullable=False)
    total_time = sq.Column(sq.Integer, nullable=False)

    breaks = relationship("Break", back_populates="break_type")

    sq.PrimaryKeyConstraint(id)
