from fastapi import APIRouter, Depends, status
import typing as tp
from dto.employee import EmployeeSchema
from services.employee import EmployeeService


EmployeeRouter = APIRouter(
    prefix="/v1/employees", tags=["employee"]
)

@EmployeeRouter.get("/", response_model=tp.List[EmployeeSchema])
def index(
    name: tp.Optional[str] = None,
    employeeService: EmployeeService = Depends()
):
    pass


@EmployeeRouter.get("/{id}", response_model=EmployeeSchema)
def get(id: str, employeeService: EmployeeService = Depends()):
    pass
