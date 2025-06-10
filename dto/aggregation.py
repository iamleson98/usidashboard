from pydantic import BaseModel
# import typing as tp
from datetime import datetime

"""
    {
        id: 1,
        updated_at: ...,
        live_attendances: [
            {
                time: ...,
                live_counts: {
                    floor_1: 23,
                    florr_2: 30,
                    floor_3: 44,
                },
            },
            {
                time: ...,
                live_counts: {
                    floor_1: 23,
                    florr_2: 30,
                    floor_3: 44,
                },
            },
        ],
    }
"""



class AttendaceRecord(BaseModel):
    time: datetime
    live_count: dict[str, int]


class AggregationSchema(BaseModel):
    id: int
    updated_at: datetime
    live_attendances: list[AttendaceRecord]
