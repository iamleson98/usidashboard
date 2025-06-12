from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
import typing as tp
from dto.checking_events import CheckingEventSchema
from repositories.checkout_events import CheckingEventRepo
# from repositories.aggregation import AggregationRepo
from services.abnormals import AggregationService
# from repositories.abnormal_checking import AbnormalCheckingRepo
# from models.aggregations import Aggregation
import asyncio
# from configs.db import get_db_connection
from configs.env import env
# from dto.common import OrderDirection
# from repositories.job import JobRepo
# import json


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
async def get_aggregations_data(socket: WebSocket, svc: AggregationService = Depends()):
    await socket.accept()
    initial = await svc.get_aggregation()
    await socket.send_json(initial.model_dump_json())

    closed = False

    try:
        while not closed:
            await asyncio.sleep(env.REAL_TIME_REPORT_INTERVAL_SECS)
            
            aggregation_data = await svc.get_aggregation()

            await socket.send_json(aggregation_data.model_dump_json())
    except WebSocketDisconnect:
        closed = True
