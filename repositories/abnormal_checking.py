# from models.employee import Employee
from repositories.base import BaseRepo
# from dto.employee import EmployeeSearch


class AbnormalCheckingRepo(BaseRepo):
    # def list_employees(self, opts: EmployeeSearch):
    #     query = self.db.query(Employee)

    #     if opts.id:
    #         query = query.filter(Employee.id == opts.id)
    #     if opts.first_name:
    #         query = query.filter(Employee.id.ilike(f"%{opts.first_name}%"))
    #     if opts.last_name:
    #         query = query.filter(Employee.last_name.ilike(f"%{opts.last_name}%"))

    #     return query.limit(opts.limit).offset(opts.offset).all()
    pass
