from models.employee import Employee
from repositories.base import BaseRepo
from dto.employee import EmployeeSearch, EmployeeOrderBy


class EmployeeRepo(BaseRepo):
    def list_employees(self, opts: EmployeeSearch):
        query = self.db.query(Employee)

        if opts.id:
            query = query.filter(Employee.id == opts.id)
        if opts.first_name:
            query = query.filter(Employee.id.ilike(f"%{opts.first_name}%"))
        if opts.last_name:
            query = query.filter(Employee.last_name.ilike(f"%{opts.last_name}%"))
        if opts.order_by and opts.order_direction:
            order_col = Employee.id
            if opts.order_by == EmployeeOrderBy.first_name:
                order_col = Employee.first_name
            elif opts.order_by == EmployeeOrderBy.last_name:
                order_col = Employee.last_name
            elif opts.order_by == Employee.department:
                order_col = Employee.department
            
            query = query.order_by(
                opts.order_direction.to_orm_operator(order_col)
            )

        return query.limit(opts.limit).offset(opts.offset).all()        
