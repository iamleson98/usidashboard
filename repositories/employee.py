# from sqlalchemy.orm import Session, lazyload
# from configs.db import get_db_connection
from models.employee import Employee
from repositories.base import BaseRepo
from dto.employee import EmployeeSearch


class EmployeeRepo(BaseRepo):
    # def get(self, id: str) -> Employee:
    #     self.db.get(
    #         Employee,
    #         id,
    #         # options=[lazyload(Employee.checking_events)]
    #     )

    def list_employees(self, opts: EmployeeSearch):
        query = self.db.query(Employee)

        if opts.id:
            query = query.filter(Employee.id == opts.id)
        if opts.first_name:
            query = query.filter(Employee.id.ilike(f"%{opts.first_name}%"))
        if opts.last_name:
            query = query.filter(Employee.last_name.ilike(f"%{opts.last_name}%"))

        return query.limit(opts.limit).offset(opts.offset).all()

    # def create(self, employee: Employee) -> Employee:
    #     self.db.add(employee)
    #     self.db.commit()
    #     self.db.refresh(employee)
    #     return employee

    # def update(self, id: str, employee: Employee) -> Employee:
    #     employee.id = id
    #     self.db.merge(employee)
    #     self.db.commit()
    #     return employee

    # def delete(self, employee: Employee) -> bool:
    #     self.db.delete(employee)
    #     self.db.commit()
    #     self.db.flush()
    #     return True
