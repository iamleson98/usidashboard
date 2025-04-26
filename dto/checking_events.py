from pydantic import BaseModel
from datetime import datetime
import typing as tp


class CheckingEventSchema(BaseModel):
    id: int
    employee_id: str
    type: int
    time: datetime


class CheckingEventSearch(BaseModel):
    ids: tp.Optional[list[int]]
    employee_id: tp.Optional[str]
    offset: tp.Optional[int]
    limit: tp.Optional[int]
