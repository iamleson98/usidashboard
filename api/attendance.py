from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
import typing as tp
from dto.checking_events import CheckingEventSchema
from dto.aggregation import AggregationSchema
from repositories.checkout_events import CheckingEventRepo
from repositories.aggregation import AggregationRepo
from models.aggregations import Aggregation
import asyncio

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
    res: Aggregation = svc.get_one()
    await socket.send_json(res.normalize().model_dump_json())

    try:
        while True:
            await asyncio.sleep(300)
            res: Aggregation = svc.get_one()
            await socket.send_json(res.normalize().model_dump_json())
    except WebSocketDisconnect:
        await socket.close()

    # return res.normalize()
