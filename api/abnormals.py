from fastapi import APIRouter, Depends, status
from datetime import datetime
import typing as tp
from repositories.abnormal_checking import AbnormalCheckingRepo

AbnormalRouter = APIRouter(
    prefix="/v1/abnormals", tags=["abnormal"]
)

@AbnormalRouter.get("/")
def get_list(
    start_time: tp.Optional[datetime] = None, 
    end_time: tp.Optional[datetime] = None,
    floor_number: int = 1,
    employee_id: str = None,
    svc: AbnormalCheckingRepo = Depends(),
    limit: int = 100,
    offset: int = 0,
):
    pass
