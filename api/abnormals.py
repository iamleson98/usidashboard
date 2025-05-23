from fastapi import APIRouter, Depends, status
from datetime import datetime
import typing as tp
from repositories.abnormal_checking import AbnormalCheckingRepo
from dto.abnormal import AbnormalChecking, AbnormalCheckingOrderBy
from dto.common import ListReturnSchema, OrderDirection
from models.abnormal_checking import AbnormalChecking as AbnormalCheckingModel


AbnormalRouter = APIRouter(
    prefix="/v1/abnormals", tags=["abnormal"]
)

@AbnormalRouter.get("/", response_model=ListReturnSchema[AbnormalChecking])
def get_list(
    start_time: tp.Optional[datetime] = None, 
    end_time: tp.Optional[datetime] = None,
    floor_number: int = 1,
    query: str = None,
    limit: int = 100,
    offset: int = 0,
    count_total: bool = False,
    order_by: AbnormalCheckingOrderBy = AbnormalCheckingOrderBy.in_time,
    order_direction: OrderDirection = OrderDirection.asc,
    svc: AbnormalCheckingRepo = Depends(),
):
    abnormal_list = svc.list_by_time(limit, offset, start_time, end_time, floor_number, query, order_by, order_direction)

    if not abnormal_list:
        return ListReturnSchema(
            total=0,
            records=[],
            status=200,
        )
    
    result = ListReturnSchema(
        records=map(lambda record: record.normalize(), abnormal_list),
        status=200,
        total=0,
        error=None,
    )

    if count_total:
        count = svc.count_by_options(start_time, end_time, floor_number, query)
        if type(count) is int:
            result.total = count

    return result
