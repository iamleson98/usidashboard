from models.base import EntityMeta
import sqlalchemy as sa
from dto.aggregation import AggregationSchema, AttendaceRecord
from datetime import datetime

date_format = "%Y-%m-%d %H:%M:%S"


class Aggregation(EntityMeta):
    __tablename__ = "aggregations"

    id = sa.Column(sa.BigInteger, nullable=False, primary_key=True, autoincrement=True)
    updated_at = sa.Column(sa.DateTime, nullable=False)
    live_attendances = sa.Column(sa.JSON)

    def normalize(self) -> AggregationSchema:
        res = AggregationSchema(id=self.id, updated_at=self.updated_at, live_attendances=[])
        time_strs: list[str] = self.live_attendances.keys()
        sorted_time_strs = sorted(time_strs, key=lambda item: datetime.strptime(item, date_format))
        
        for item in sorted_time_strs:
            actual_time = datetime.strptime(item, date_format)
            record = AttendaceRecord(
                time=actual_time,
                live_count=self.live_attendances[item],
            )
            res.live_attendances.append(record)

        return res

