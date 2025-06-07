from pydantic import BaseModel
import typing as tp
from datetime import datetime


class AttendaceRecord(BaseModel):
    time: datetime
    live_count: int


class AggregationSchema(BaseModel):
    id: int
    updated_at: datetime
    live_attendances: list[AttendaceRecord]
