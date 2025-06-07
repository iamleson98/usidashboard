from repositories.base import BaseRepo
from models.aggregations import Aggregation


class AggregationRepo(BaseRepo):
    def get_one(self):
        aggs = self.db.query(Aggregation).limit(1).all()
        if len(aggs) == 0:
            return None
        return aggs[0]   
