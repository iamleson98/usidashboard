from fastapi import APIRouter, Depends, status
import typing as tp
from dto.employee import EmployeeSchema
from services.employee import EmployeeService


BreakApiRouter = APIRouter(
    prefix="/v1/breaks", tags=["break"]
)
