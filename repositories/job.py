from repositories.base import BaseRepo
from models.job import Job
import sqlalchemy as sq


class JobRepo(BaseRepo):
    def get_last_job(self, only_success: bool = False):
        """returns the most recent job"""
        query = self.db.query(Job)

        if only_success:
            query = query.filter(Job.status == True)

        return query.order_by(sq.desc(Job.execution_at)).first()
