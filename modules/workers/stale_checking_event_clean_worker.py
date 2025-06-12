from modules.workers.base_worker import BaseWorker
from repositories.checkout_events import CheckingEventRepo
from datetime import datetime, timedelta


class StaleCheckingEventsWorker(BaseWorker):
    """
    This worker 
    """
    name = "StaleCheckingEventsWorker"

    def __init__(self):
        super().__init__()
        self.checkingEventRepo = CheckingEventRepo(self.db)

    def execute(self):
        now = datetime.now()
        last_12_hours = now - timedelta(hours=12)

        try:
            self.checkingEventRepo.delete_records_before_time(last_12_hours)
            self.set_job_success(self.name)
        except Exception as e:
            self.set_job_error(self.name, f"{e}")


def clear_stale_events():
    wk = StaleCheckingEventsWorker()
    wk.execute()
