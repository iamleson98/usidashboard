from models.base import EntityMeta
import sqlalchemy as sq
from sqlalchemy.orm import relationship
from dto.checking_events import CheckingEventSchema


class CheckingEvent(EntityMeta):
    __tablename__ = "checking_events"

    id = sq.Column(sq.BigInteger, nullable=False, primary_key=True, autoincrement=True)
    employee_id = sq.Column(sq.String(length=12), sq.ForeignKey("employees.id"))
    type = sq.Column(sq.SmallInteger, nullable=True)
    time = sq.Column(sq.DateTime, nullable=False)

    employee = relationship(
        "Employee",
        back_populates="checking_events",
    )

    sq.PrimaryKeyConstraint(id)

    def normalize(self):
        return CheckingEventSchema(
            id=self.id,
            employee_id=self.employee_id,
            type=self.type,
            time=self.time
        )
