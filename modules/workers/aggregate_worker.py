from modules.workers.base_worker import BaseWorker
from datetime import date, datetime
from repositories.checkout_events import CheckoutEventRepo
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
        self.checkingEventRepo = CheckoutEventRepo(self.db)
        self.employeeRepo = EmployeeRepo(self.db)

    def execute(self, date_to_run: date):
        start_time = datetime(
            year=date_to_run.year, 
            month=date_to_run.month,
            day=date_to_run.day,
            hour=0,
            min=0,
            second=0,
        )
        end_time = datetime(
            year=date_to_run.year, 
            month=date_to_run.month,
            day=date_to_run.day,
            hour=23,
            min=59,
            second=59,
        )

        has_more_job = True
        offset = 0

        while has_more_job:
            try:
                checking_events = self.checkingEventRepo.list_by_time(start_time, end_time, self.BATCH, offset, True)
            except Exception as e:
                self.set_job_error(self.NAME, e)
                return

            has_more_job = checking_events and len(checking_events) == self.BATCH
            offset += len(checking_events)


            meet_map = {}

            for event in checking_events:
                if event and event.is_checkin: # check in
                    if meet_map.get(event.employee_id, None) is None:
                        meet_map[event.employee_id] = 1
                        continue
                    if meet_map.get(event.employee_id, None) == 0:
                        pass


                # if event and event.type == 0
