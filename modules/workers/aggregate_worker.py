from modules.workers.base_worker import BaseWorker
from datetime import date, datetime
from repositories.checkout_events import CheckingEventRepo
from repositories.employee import EmployeeRepo


class DataAggregateWorker(BaseWorker):
    NAME = "DataAggregateWorker"
    BATCH = 500
    OFFSET = 0
    IN_VALID_SECONDS = 10 * 60

    def __init__(
        self,
    ):
        super().__init__()
        # self.date_to_run = date_to_run
        self.checkingEventRepo = CheckingEventRepo(self.db)
        self.employeeRepo = EmployeeRepo(self.db)

    def execute(self, date_to_run: date):
        now = datetime.now()
        
