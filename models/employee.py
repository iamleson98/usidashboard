from models.base import EntityMeta
import sqlalchemy as sq
from sqlalchemy.orm import relationship
from dto.employee import EmployeeSchema


class Employee(EntityMeta):
    __tablename__ = "employees"

    id = sq.Column(sq.String(length=12), nullable=False, primary_key=True)
    first_name = sq.Column(sq.String(length=255), nullable=False)
    last_name = sq.Column(sq.String(length=255), nullable=False)
    card_no = sq.Column(sq.String(length=20), nullable=False)
    is_visitor = sq.Column(sq.Boolean, nullable=True, default=False)
    department = sq.Column(sq.String(500), nullable=False)

    checking_events = relationship('CheckingEvent', back_populates='employee')
    abnormals = relationship(
        "AbnormalChecking",
        back_populates="employee",
    )

    sq.PrimaryKeyConstraint(id)

    def normalize(self):
        """normalize returns basic information of an employee"""
        return EmployeeSchema(
            id=self.id,
            first_name=self.first_name,
            last_name=self.last_name,
            card_no=self.card_no,
            is_visitor=self.is_visitor,
            department=self.department,
        )
    
    @staticmethod
    def from_dto(employee: EmployeeSchema) -> "Employee":
        return Employee(
            id=employee.id,
            first_name=employee.first_name,
            last_name=employee.last_name,
            card_no=employee.card_no,
            is_visitor=employee.is_visitor,
            department=employee.department,
        )
