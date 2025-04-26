from repositories.job import JobRepo
from fastapi import Depends
from services.base import BaseService

class JobService(BaseService):
    jobRepo: JobRepo

    def __init__(self, jobRepo: JobRepo = Depends()):
        self.jobRepo = jobRepo
        super().__init__()

    def get_latest_job(self):
        return self.jobRepo.get_last_job()

