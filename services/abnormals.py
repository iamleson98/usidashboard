from fastapi import Depends
# import typing as tp
from services.base import BaseService
from repositories.aggregation import AggregationRepo
from modules.workers.data_crawler import DATA_FOLDER_PATH, CRAWLER_WORKER
import os
# import asyncio


class AggregationService(BaseService):
    repo: AggregationRepo

    def __init__(self, repo: AggregationRepo = Depends()):
        self.repo = repo
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

        # results = [(CRAWLER_WORKER.handle_data(file), CRAWLER_WORKER.handle_aggregate(file)) for file in stray_data_files]
        for file in stray_data_files:
            err1 = CRAWLER_WORKER.handle_data(file)
            err2 = CRAWLER_WORKER.handle_aggregate(file)

            if not err1 and not err2:
                CRAWLER_WORKER.handle_delete_file(file)

        return True
