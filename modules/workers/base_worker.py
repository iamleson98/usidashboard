from models.job import Job
from repositories.job import JobRepo
from configs.db import get_db_connection
from datetime import datetime


class BaseWorker:
    def __init__(self):
        self.db = next(get_db_connection())
        self.jobRepo = JobRepo(self.db)

    def set_job_error(self, job_type: str, reason: str):
        new_job = Job(job_type=job_type, status=False, reason=reason, execution_at=datetime.now())
        self.jobRepo.create(new_job)

    def set_job_success(self, job_type: str):
        new_job = Job(job_type=job_type, status=True, execution_at=datetime.now())
        self.jobRepo.create(new_job)
