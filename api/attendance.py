from fastapi import APIRouter, Depends, status
import typing as tp
# from dto.employee import EmployeeSchema
from dto.checking_events import CheckingEventSchema, CheckingEventSearch
from services.checking_event import CheckingEventService


CheckingEventApiRouter = APIRouter(
    prefix="/v1/checking_events", tags=["checking_events"]
)

# @CheckingEventApiRouter.get("/", response_model=tp.List[CheckingEventSchema])
# async def search_checking_events(
#     search_opts: CheckingEventSearch,
#     svc: CheckingEventService
# ):
#     checking_events = svc.find_checking_events_by_employee(search_opts.employee_id[0])
#     return [
#         evt.normalize()
#         for evt in checking_events
#     ]
