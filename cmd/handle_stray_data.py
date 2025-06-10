
from repositories.aggregation import AggregationRepo
from configs.db import get_db_connection

from services.abnormals import AggregationService


repo = AggregationRepo(next(get_db_connection()))

svc = AggregationService(repo=repo)

svc.handle_stray_data_files()
