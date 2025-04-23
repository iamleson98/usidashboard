from models.base import EntityMeta
import sqlalchemy as sq
from sqlalchemy.orm import relationship

class Employee(EntityMeta):
    __tablename__ = "employees"

    id = sq.Column(sq.String(length=12), nullable=False, primary_key=True)
    first_name = sq.Column(sq.String(length=255), nullable=False)
    last_name = sq.Column(sq.String(length=255), nullable=False)
    card_no = sq.Column(sq.String(length=20), nullable=False)
    is_visitor = sq.Column(sq.Boolean, nullable=True, default=False)
    department = sq.Column(sq.String(500), nullable=False)

    checking_events = relationship('CheckingEvent', back_populates='employee')

    sq.PrimaryKeyConstraint(id)
