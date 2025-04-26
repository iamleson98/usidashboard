from fastapi import APIRouter, Depends
import typing as tp
from dto.checking_events import CheckingEventSchema, CheckingEventSearch
from services.checking_event import CheckingEventService


CheckingEventApiRouter = APIRouter(
    prefix="/v1/checking_events", tags=["checking_events"]
)

@CheckingEventApiRouter.get("/", response_model=tp.List[CheckingEventSchema])
async def search_checking_events(
    offset: tp.Optional[int] = 0,
    limit: tp.Optional[int] = 100,
    employee_id: tp.Optional[int] = None,
    # ids: tp.Optional[tp.List[int]] = None,
    svc: CheckingEventService = Depends()
):
    checking_events = svc.find_checking_events_by_employee(employee_id, offset, limit)
    return [
        evt.normalize()
        for evt in checking_events
    ]
