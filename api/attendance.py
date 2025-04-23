from fastapi import APIRouter, Depends, status
import typing as tp
from dto.employee import EmployeeSchema
from services.employee import EmployeeService


CheckingEventApiRouter = APIRouter(
    prefix="/v1/checking_events", tags=["checking_events"]
)
