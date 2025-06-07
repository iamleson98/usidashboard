from repositories.base import BaseRepo
from models.checking_event import CheckingEvent
import typing as tp
from datetime import datetime
from sqlalchemy import desc, asc


class CheckingEventRepo(BaseRepo):
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
    
    def dedup_data(self):
        """we dont allow duplication on the 3 fields (employee_id, is_checkin, time) of table checking_events"""

        TABLE_NAME = "checking_events"
        employee_id = "employee_id"
        is_checkin = "is_checkin"
        time = "time"

        query = f"""
        WITH CTE AS (
            SELECT
                {employee_id},
                {is_checkin},
                {time},
                ROW_NUMBER() OVER (PARTITION BY {employee_id}, {is_checkin}, {time} ORDER BY {time}) as row_num
            FROM {TABLE_NAME}
        )
        DELETE FROM {TABLE_NAME}
        WHERE ({employee_id}, {is_checkin}, {time}) IN (
            SELECT
                {employee_id},
                {is_checkin},
                {time}
            FROM CTE
            WHERE row_num > 1
        )
        """
        try:
            self.db.execute(query)
            self.db.commit()
        except Exception:
            self.db.rollback()

    def find_last_checking_event_by_employee_id(self, id: str, check_in = False):
        """returns the latest check in/out event of given employee"""
        checking_events = self.db.query(CheckingEvent).\
            filter(CheckingEvent.is_checkin == check_in, CheckingEvent.employee_id == id).\
                order_by(desc(CheckingEvent.time)).limit(1).all()

        if len(checking_events):
            return checking_events[0]
        return None
    
    def delete_records_before_time(self, time: datetime) -> int:
        return self.db.query(CheckingEvent).filter(CheckingEvent.time < time).delete()
    
