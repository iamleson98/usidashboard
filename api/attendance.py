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
    closed = False
    await socket.accept()
    try:
        while True:
            await asyncio.sleep(5)
            res: Aggregation = svc.get_by_id(1, Aggregation)
            if not closed:
                await socket.send_json(res.normalize().model_dump_json())
            # await socket.send_json({'lol': 1})
    except WebSocketDisconnect:
        closed = True
        await socket.close()

    # return res.normalize()
