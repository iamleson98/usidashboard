from models.base import EntityMeta
import sqlalchemy as sq
from sqlalchemy.orm import relationship

class Break(EntityMeta):
    __tablename__ = "breaks"

    id = sq.Column(sq.String(length=12), nullable=False, primary_key=True)
    employee_id = sq.Column(sq.String(length=12), sq.ForeignKey("employees.id"),nullable=False)
    in_time = sq.Column(sq.DateTime, nullable=False)
    out_time = sq.Column(sq.DateTime, nullable=False)
    minutes = sq.Column(sq.Integer, nullable=False)
    break_type_id = sq.Column(sq.Integer, sq.ForeignKey("break_types.id"), nullable=False)

    break_type = relationship("BreakType", back_populates="breaks")
    employee = relationship("Employee", back_populates="breaks")

    sq.PrimaryKeyConstraint(id)

