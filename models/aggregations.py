from models.base import EntityMeta
import sqlalchemy as sa
from dto.aggregation import AggregationSchema, AttendaceRecord
from datetime import datetime
import json

DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


class Aggregation(EntityMeta):
    __tablename__ = "aggregations"

    id = sa.Column(sa.BigInteger, nullable=False, primary_key=True, autoincrement=True)
    updated_at = sa.Column(sa.DateTime, nullable=False)
    live_attendances = sa.Column(sa.JSON)

    def normalize(self) -> AggregationSchema:
        # print(type(self.live_attendances))
        # if type(self.live_attendances) is str:
        #     live_attendances = json.loads(self.live_attendances)
        # else:
        #     live_attendances = self.live_attendances
        records = []
        for item in self.live_attendances:
            if type(item) is str:
                item = json.loads(item)

            records.append(AttendaceRecord(time=item['time'], live_count=item['live_count']))
        # live_attendances = map(lambda item: AttendaceRecord(time=item['time'], live_count=item['live_count']), self.live_attendances)
        res = AggregationSchema(id=self.id, updated_at=self.updated_at, live_attendances=records)
        return res
    
    @staticmethod
    def from_schema(schema: AggregationSchema):
        records = map(lambda item: item.model_dump_json(), schema.live_attendances)
        res = Aggregation(
            id=schema.id,
            updated_at=schema.updated_at,
            live_attendances=list(records),
        )
        return res

