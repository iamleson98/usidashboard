from repositories.base import BaseRepo
from datetime import datetime
from models.abnormal_checking import AbnormalChecking
from sqlalchemy import desc


class AbnormalCheckingRepo(BaseRepo):
    def list_by_time(self, limit: int = 100, offset: int = 0, start_time: datetime = None, end_time: datetime = None):
        query = self.db.query(AbnormalChecking)

        if (start_time):
            query = query.filter(AbnormalChecking.out_time >= start_time)
        if (end_time):
            query = query.filter(AbnormalChecking.in_time <= end_time)

        if limit > 0:
            query = query.limit(limit)
        if offset >= 0:
            query = query.offset(offset)

        return query.order_by(desc(AbnormalChecking.out_time)).all()

    def list_by_employee_id(self, employee_id: str, limit: int = 100, offset: int = 0, start_time: datetime = None, end_time: datetime = None):
        results_by_time = self.list_by_time(limit, offset, start_time, end_time)
        return filter(lambda item: item.employee_id == employee_id, results_by_time)
