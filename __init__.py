from repositories.aggregation import AggregationRepo
from configs.db import get_db_connection

from services.abnormals import AggregationService
import asyncio


repo = AggregationRepo(next(get_db_connection()))

svc = AggregationService(repo=repo)

if __name__ == "__main__":
    async def main():
        await svc.handle_stray_data_files()

    asyncio.run(main())