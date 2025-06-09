from repositories.base import BaseRepo
from models.aggregations import Aggregation


class AggregationRepo(BaseRepo):
    def get_one(self):
        return self.db.query(Aggregation).first()
