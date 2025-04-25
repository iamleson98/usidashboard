from fastapi import APIRouter, Depends, status
import typing as tp
from dto.employee import EmployeeSchema
from services.employee import EmployeeService


EmployeeRouter = APIRouter(
    prefix="/v1/employees", tags=["employee"]
)

@EmployeeRouter.get("/", response_model=tp.List[EmployeeSchema])
def list(
    name: tp.Optional[str] = None,
    employeeService: EmployeeService = Depends()
):
    pass


@EmployeeRouter.get("/{id}", response_model=EmployeeSchema)
def get(id: str, svc: EmployeeService = Depends()):
    return svc.get_by_id(id).normalize()


@EmployeeRouter.post("/", response_model=EmployeeSchema, status_code=status.HTTP_201_CREATED)
def create(
    employee: EmployeeSchema,
    svc: EmployeeService = Depends(),
):
    return svc.create(employee)
