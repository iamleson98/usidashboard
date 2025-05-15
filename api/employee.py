from fastapi import APIRouter, Depends, status
import typing as tp
from dto.employee import EmployeeSchema
# from services.employee import EmployeeService
from repositories.employee import EmployeeRepo
from models.employee import Employee
from dto.employee import EmployeeSearch, EmployeeOrderBy
from dto.common import OrderDirection


EmployeeRouter = APIRouter(
    prefix="/v1/employees", tags=["employee"]
)

@EmployeeRouter.get("/", response_model=tp.List[EmployeeSchema])
def list(
    id: tp.Optional[str] = None,
    first_name: tp.Optional[str] = None,
    last_name: tp.Optional[str] = None,
    limit: int = 50,
    offset: int = 0,
    order_by: tp.Optional[EmployeeOrderBy] = EmployeeOrderBy.first_name,
    order_direction: tp.Optional[OrderDirection] = OrderDirection.asc,
    svc: EmployeeRepo = Depends()
):
    params = EmployeeSearch(
        id=id,
        first_name=first_name,
        last_name=last_name,
        limit=limit,
        offset=offset,
        order_by=order_by,
        order_direction=order_direction,
    )
    employees = svc.list_employees(params)
    if not employees or len(employees) == 0:
        return []
    return map(lambda emp: emp.normalize(), employees)

@EmployeeRouter.get("/{id}", response_model=tp.Optional[EmployeeSchema])
def get(id: str, svc: EmployeeRepo = Depends()):
    employee: Employee = svc.get_by_id(id, Employee)
    if employee:
        return employee.normalize()
    return None


@EmployeeRouter.post("/", response_model=EmployeeSchema, status_code=status.HTTP_201_CREATED)
def create(
    employee: EmployeeSchema,
    svc: EmployeeRepo = Depends(),
):
    if employee.is_valid() is None:
        return svc.create(Employee.from_dto(employee)).normalize()
    return None
