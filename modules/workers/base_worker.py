from services.job import JobService
from models.job import Job


class BaseWorker:
    def __init__(self):
        self.jobSvc = JobService()

    def set_job_error(self, job_type: str, reason: str):
        new_job = Job(job_type=job_type, status=False, reason=reason)
        self.jobSvc.create(new_job)

    def set_job_success(self, job_type: str):
        new_job = Job(job_type=job_type, status=True)
        self.jobSvc.create(new_job)
