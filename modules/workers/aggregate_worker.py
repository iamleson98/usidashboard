from modules.workers.base_worker import BaseWorker
from datetime import date, datetime, timedelta
from repositories.checkout_events import CheckingEventRepo
from repositories.employee import EmployeeRepo
from repositories.abnormal_checking import AbnormalCheckingRepo
from collections import defaultdict
import calendar

class DataAggregateWorker(BaseWorker):
    NAME = "DataAggregateWorker"
    BATCH = 500
    OFFSET = 0
    IN_VALID_SECONDS = 10 * 60

    def __init__(
        self,
    ):
        super().__init__()
        self.checkingEventRepo = CheckingEventRepo(self.db)
        self.employeeRepo = EmployeeRepo(self.db)
        self.abnormalRepo = AbnormalCheckingRepo(self.db)

    def __aggregate_for_this_week(self):
        now = datetime.now()
        last_7_days = now - timedelta(days=7)

        has_more_records = True
        offset = 0

        abnormals_by_employee = defaultdict(list)

        while has_more_records:
            abnormal_cases = self.abnormalRepo.list_by_time(limit=self.BATCH, offset=offset, start_time=last_7_days, end_time=now)

            has_more_records = len(abnormal_cases) == self.BATCH
            offset += len(abnormal_cases)

            for record in abnormal_cases:
                abnormals_by_employee[record.employee_id].append(record.total_mins)

        # calendar.week

    def execute(self):
        now = datetime.now()


def run_aggregation_job():
    worker = DataAggregateWorker()
    worker.execute()
