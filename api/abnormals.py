from fastapi import APIRouter, Depends, status
from datetime import datetime
import typing as tp
from repositories.abnormal_checking import AbnormalCheckingRepo
from dto.abnormal import AbnormalChecking

AbnormalRouter = APIRouter(
    prefix="/v1/abnormals", tags=["abnormal"]
)

@AbnormalRouter.get("/", response_model=tp.List[AbnormalChecking])
def get_list(
    start_time: tp.Optional[datetime] = None, 
    end_time: tp.Optional[datetime] = None,
    floor_number: int = 1,
    employee_id: str = None,
    limit: int = 100,
    offset: int = 0,
    svc: AbnormalCheckingRepo = Depends(),
):
    abnormal_list = svc.list_by_time(limit=limit, offset=offset, start_time=start_time, end_time=end_time, floor_number=floor_number)
    if not abnormal_list:
        return []
    
    return map(lambda record: record.normalize(), abnormal_list)
