from sqlalchemy.orm import Session, lazyload
from configs.db import get_db_connection
from models.employee import Employee
from repositories.base import BaseRepo


class EmployeeRepo(BaseRepo):
    def get(self, id: str) -> Employee:
        self.db.get(
            Employee,
            id,
            # options=[lazyload(Employee.checking_events)]
        )

    def create(self, employee: Employee) -> Employee:
        self.db.add(employee)
        self.db.commit()
        self.db.refresh(employee)
        return employee
