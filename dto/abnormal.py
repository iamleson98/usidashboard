from datetime import datetime
from pydantic import BaseModel
from enum import Enum


class AbnormalChecking(BaseModel):
    id: int
    employee_id: str
    in_time: datetime
    out_time: datetime
    total_mins: int
    checkin_station: str
    checkout_station: str


class AbnormalCheckingOrderBy(Enum):
    in_time = "in_time"
    out_time = "out_time"
    total_mins = "total_mins"