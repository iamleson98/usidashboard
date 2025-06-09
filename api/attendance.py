from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
import typing as tp
from dto.checking_events import CheckingEventSchema
# from dto.aggregation import AggregationSchema
from repositories.checkout_events import CheckingEventRepo
from repositories.aggregation import AggregationRepo
from models.aggregations import Aggregation
import asyncio
from configs.db import get_db_connection

CheckingEventApiRouter = APIRouter(
    prefix="/v1/checking-events", tags=["checking_events"]
)

@CheckingEventApiRouter.get("/", response_model=tp.List[CheckingEventSchema])
async def search_checking_events(
    offset: tp.Optional[int] = 0,
    limit: tp.Optional[int] = 100,
    employee_id: tp.Optional[int] = None,
    svc: CheckingEventRepo = Depends()
):
    checking_events = svc.find_by_employee_id(employee_id, offset, limit)
    return [
        evt.normalize()
        for evt in checking_events
    ]


@CheckingEventApiRouter.websocket("/live-attendances")
async def get_aggregations_data(socket: WebSocket, svc: AggregationRepo = Depends()):
    await socket.accept()
    initial: Aggregation = svc.get_one()
    await socket.send_json(initial.normalize().model_dump_json())

    closed = False

    try:
        while not closed:
            await asyncio.sleep(10)
            res: Aggregation = AggregationRepo(next(get_db_connection())).get_one()
            await socket.send_json(res.normalize().model_dump_json())
    except WebSocketDisconnect:
        closed = True
