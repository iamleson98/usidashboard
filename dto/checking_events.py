from pydantic import BaseModel
from datetime import time
import typing as tp

class CheckingEventSchema(BaseModel):
    id: int
    employee_id: str
    in_time: tp.Optional[time]
    out_time: tp.Optional[time]
    minutes: float
    break_type_id: int


class CheckingEventSearch(BaseModel):
    ids: tp.Optional[list[int]]
    employee_id: tp.Optional[str]
