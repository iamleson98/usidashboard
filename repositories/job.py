from repositories.base import BaseRepo
from models.job import Job
import sqlalchemy as sq

class JobRepo(BaseRepo):
    def get_last_job(self):
        """returns the most recent job"""
        return self.db.query(Job).order_by(sq.desc(Job.execution_at)).first()
