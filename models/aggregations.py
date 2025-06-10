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
        live_attendances = json.loads(self.live_attendances)
        live_attendances = map(lambda item: json.loads(item), live_attendances)
        # live_attendances = map(lambda item: datetime.fromisoformat(item["time"]), live_attendances)
        res = AggregationSchema(id=self.id, updated_at=self.updated_at, live_attendances=list(live_attendances))
        return res
    
    @staticmethod
    def from_schema(schema: AggregationSchema):
        records = map(lambda item: item.model_dump_json(), schema.live_attendances)
        res = Aggregation(
            id=schema.id,
            updated_at=schema.updated_at,
            live_attendances=json.dumps(list(records)),
        )
        # data = {}
        # for item in schema.live_attendances:
        return res

