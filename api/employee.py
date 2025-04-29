from fastapi import APIRouter, Depends, status
import typing as tp
from dto.employee import EmployeeSchema
# from services.employee import EmployeeService
from repositories.employee import EmployeeRepo
from models.employee import Employee


EmployeeRouter = APIRouter(
    prefix="/v1/employees", tags=["employee"]
)

@EmployeeRouter.get("/", response_model=tp.List[EmployeeSchema])
def list(
    name: tp.Optional[str] = None,
    employeeService: EmployeeRepo = Depends()
):
    pass

@EmployeeRouter.get("/{id}", response_model=EmployeeSchema)
def get(id: str, svc: EmployeeRepo = Depends()):
    return svc.get_by_id(id, Employee).normalize()


@EmployeeRouter.post("/", response_model=EmployeeSchema, status_code=status.HTTP_201_CREATED)
def create(
    employee: EmployeeSchema,
    svc: EmployeeRepo = Depends(),
):
    if employee.is_valid():
        return svc.create(Employee.from_dto(employee))
    return None
