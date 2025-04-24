from fastapi import Depends
from repositories.employee import EmployeeRepo
from models.employee import Employee
from dto.employee import EmployeeSchema
import typing as tp
from utils.types import Error


class EmployeeService:
    employeeRepo: EmployeeRepo

    def __init__(self, employeeRepo: EmployeeRepo = Depends()):
        self.employeeRepo = employeeRepo

    def create(self, employee_body: EmployeeSchema) -> tp.Union[Employee, Error]:
        err = employee_body.is_valid()
        if err:
            return err

        return self.employeeRepo.create(
            Employee(**employee_body)
        )
    
    def bulk_create(self, employees: tp.List[EmployeeSchema]) -> tp.List[EmployeeSchema]:
        pass

    def get_by_id(self, id: str) -> Employee:
        return self.employeeRepo.get_by_id(id, Employee)