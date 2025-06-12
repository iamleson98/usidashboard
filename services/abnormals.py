from fastapi import Depends
from services.base import BaseService
from repositories.aggregation import AggregationRepo
from modules.workers.data_crawler import DATA_FOLDER_PATH, DataCrawlerWorker
import os
from repositories.abnormal_checking import AbnormalCheckingRepo
from dto.aggregation import AggregationResponse
from dto.common import OrderDirection
from repositories.job import JobRepo
from configs.db import get_db_connection


class AggregationService(BaseService):
    repo: AggregationRepo

    def __init__(self, repo: AggregationRepo = Depends(), abnormalRepo: AbnormalCheckingRepo = Depends(), jobRepo: JobRepo = Depends()):
        self.repo = repo
        self.abnormalRepo = abnormalRepo
        self.jobRepo = jobRepo
        super().__init__()

    async def handle_stray_data_files(self):
        """This method handles all the raw data files that is not handled and remain in the file system."""
        stray_data_files = []
        entities = os.listdir(DATA_FOLDER_PATH)

        for entity in entities:
            entity_path = os.path.join(DATA_FOLDER_PATH, entity)
            if not os.path.isdir(entity_path) or not entity.startswith("Identity Access Search"):
                continue

            entity_files = os.listdir(entity_path)
            stray_data_files.extend(map(lambda item: os.path.splitext(item)[0], entity_files))

        worker = DataCrawlerWorker()

        for file in stray_data_files:
            err1 = worker.handle_data(file)
            err2 = worker.handle_aggregate(file)

            if not err1 and not err2:
                worker.handle_delete_file(file)

        return True

    async def get_aggregation(self) -> AggregationResponse:
        session = next(get_db_connection())

        repo = AggregationRepo(session)
        abnormalRepo = AbnormalCheckingRepo(session)
        abnormal_cases = abnormalRepo.list_by_time(limit=50, order_direction=OrderDirection.desc)

        aggregation = repo.get_one()

        if not aggregation:
            session.close()
            return AggregationResponse(aggregations=None, abnormal_cases=[])
        
        abnormal_cases = list(map(lambda item: item.normalize(), abnormal_cases))

        session.close()

        return AggregationResponse(
            aggregations=aggregation.normalize(),
            abnormal_cases=abnormal_cases,
        )
