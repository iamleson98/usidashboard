from repositories.base import BaseRepo
from models.checking_event import CheckingEvent
import typing as tp


class CheckoutEventRepo(BaseRepo):
    def find_by_employee_id(self, employee_id: str, offset: int = 0, limit: int = 100) -> tp.List[CheckingEvent]:
        query = self.db.query(CheckingEvent).\
            filter(CheckingEvent.employee_id == employee_id)
        if offset:
            query = query.offset(offset)
        if limit:
            query = query.limit(limit)

        return query.all()
