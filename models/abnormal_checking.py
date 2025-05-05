from models.base import EntityMeta
import sqlalchemy as sq
from sqlalchemy.orm import relationship
# from dto.checking_events import CheckingEventSchema


class AbnormalChecking(EntityMeta):
    __tablename__ = "abnormals"

    id = sq.Column(sq.BigInteger, nullable=False, primary_key=True, autoincrement=True)
    employee_id = sq.Column(sq.String(length=12), sq.ForeignKey("employees.id"))
    in_time = sq.Column(sq.DateTime, nullable=False) # 1 means checking in, 0 mean checking out
    out_time = sq.Column(sq.DateTime, nullable=False)
    total_mins = sq.Column(sq.Integer, nullable=False)

    employee = relationship(
        "Employee",
        back_populates="abnormals",
    )

    sq.PrimaryKeyConstraint(id)

    # def normalize(self):
    #     return CheckingEventSchema(
    #         id=self.id,
    #         employee_id=self.employee_id,
    #         is_checkin=self.is_checkin,
    #         time=self.time
    #     )

