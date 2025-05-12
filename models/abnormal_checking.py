from models.base import EntityMeta
import sqlalchemy as sq
from sqlalchemy.orm import relationship
from dto.abnormal import AbnormalChecking


class AbnormalChecking(EntityMeta):
    __tablename__ = "abnormals"

    id = sq.Column(sq.BigInteger, nullable=False, primary_key=True, autoincrement=True)
    employee_id = sq.Column(sq.String(length=12), sq.ForeignKey("employees.id"))
    in_time = sq.Column(sq.DateTime, nullable=False) # 1 means checking in, 0 mean checking out
    out_time = sq.Column(sq.DateTime, nullable=False)
    total_mins = sq.Column(sq.Integer, nullable=False)
    checkin_station = sq.Column(sq.String(100), nullable=False)
    checkout_station = sq.Column(sq.String(100), nullable=False)

    employee = relationship(
        "Employee",
        back_populates="abnormals",
    )

    sq.PrimaryKeyConstraint(id)

    def normalize(self):
        return AbnormalChecking(
            id=self.id,
            employee_id=self.employee_id,
            in_time=self.in_time,
            out_time=self.out_time,
            total_mins=self.total_mins,
            checkin_station=self.checkin_station,
            checkout_station=self.checkout_station,
        )

