from repositories.base import BaseRepo
from models.checking_event import CheckingEvent
import typing as tp
from datetime import datetime
from sqlalchemy import desc, asc


class CheckoutEventRepo(BaseRepo):
    def find_by_employee_id(self, employee_id: str, offset: int = 0, limit: int = 100) -> tp.List[CheckingEvent]:
        query = self.db.query(CheckingEvent).\
            filter(CheckingEvent.employee_id == employee_id)
        if offset:
            query = query.offset(offset)
        if limit:
            query = query.limit(limit)

        return query.all()
    
    def list_by_time(self, start_time: datetime, end_time: datetime, limit: int, offset: int = 0, order_asc: bool = False, order_desc: bool = False):
        query = self.db.query(CheckingEvent)
        if start_time:
            query = query.filter(CheckingEvent.time >= start_time)
        if end_time:
            query = query.filter(CheckingEvent.time <= end_time)
        if offset >= 0:
            query = query.offset(offset)
        if limit >= 0:
            query = query.limit(limit)

        if order_asc:
            query = query.order_by(asc(CheckingEvent.time))
        elif order_desc:
            query = query.order_by(desc(CheckingEvent.time))

        return query.all()
