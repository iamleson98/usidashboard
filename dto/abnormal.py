from datetime import datetime
from pydantic import BaseModel
from enum import Enum
import typing as tp


class AbnormalChecking(BaseModel):
    id: int
    employee_id: str
    in_time: datetime
    out_time: datetime
    total_mins: int
    checkin_station: str
    checkout_station: str
    first_name: tp.Optional[str] = None
    last_name: tp.Optional[str] = None
    department: tp.Optional[str] = None


class AbnormalCheckingOrderBy(Enum):
    in_time = "in_time"
    out_time = "out_time"
    total_mins = "total_mins"