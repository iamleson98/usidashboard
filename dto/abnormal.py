from datetime import datetime
from pydantic import BaseModel

class AbnormalChecking(BaseModel):
    id: int
    employee_id: str
    in_time: datetime
    out_time: datetime
    total_mins: int
    checkin_station: str
    checkout_station: str
