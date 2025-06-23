from fastapi import APIRouter, Depends
from datetime import datetime
import typing as tp
from repositories.abnormal_checking import AbnormalCheckingRepo
from dto.abnormal import AbnormalChecking, AbnormalCheckingOrderBy
from dto.common import ListReturnSchema, OrderDirection
from dto.employee import ShortDepartment
from services.abnormals import AggregationService

AbnormalRouter = APIRouter(
    prefix="/v1/abnormals", tags=["abnormal"]
)

@AbnormalRouter.get("/", response_model=ListReturnSchema[AbnormalChecking])
def get_list(
    start_time: tp.Optional[datetime] = None, 
    end_time: tp.Optional[datetime] = None,
    floor_number: int = 1,
    query: str | None = None,
    limit: int = 100,
    offset: int = 0,
    count_total: bool = False,
    order_by: AbnormalCheckingOrderBy = AbnormalCheckingOrderBy.in_time,
    order_direction: OrderDirection = OrderDirection.asc,
    department: ShortDepartment | None = None,
    svc: AbnormalCheckingRepo = Depends(),
):
    abnormal_list = svc.list_by_time(limit, offset, start_time, end_time, floor_number, query, department, order_by, order_direction)

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
        count = svc.count_by_options(start_time, end_time, floor_number, query, department)
        if type(count) is int:
            result.total = count

    return result

@AbnormalRouter.post("/handle-stray-data-files", response_model=bool)
async def handle_stray_data_files(svc: AggregationService = Depends()):
    return await svc.handle_stray_data_files()
