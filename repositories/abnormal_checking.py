from repositories.base import BaseRepo
from datetime import datetime
from models.abnormal_checking import AbnormalChecking
from sqlalchemy import or_
from models.employee import Employee
from dto.abnormal import AbnormalCheckingOrderBy
from dto.common import OrderDirection
from dto.employee import ShortDepartment


class AbnormalCheckingRepo(BaseRepo):
    def list_by_time(
        self, 
        limit: int = 100, 
        offset: int = 0, 
        start_time: datetime = None, 
        end_time: datetime = None, 
        floor_number: int = 1, 
        search_query: str = None,
        department: ShortDepartment = None,
        order_by: AbnormalCheckingOrderBy = AbnormalCheckingOrderBy.in_time,
        order_direction: OrderDirection = OrderDirection.asc,
    ):
        query = self.__general_query_builder(
            start_time,
            end_time,
            floor_number,
            search_query,
            department,
            order_by,
            order_direction,
        )

        if limit > 0:
            query = query.limit(limit)
        if offset >= 0:
            query = query.offset(offset)

        return query.all()

    def list_by_employee_id(self, employee_id: str, limit: int = 100, offset: int = 0, start_time: datetime = None, end_time: datetime = None):
        results_by_time = self.list_by_time(limit, offset, start_time, end_time)
        return filter(lambda item: item.employee_id == employee_id, results_by_time)
    
    def __general_query_builder(
            self,
            start_time: datetime = None, 
            end_time: datetime = None, 
            floor_number: int = 1, 
            search_query: str = None,
            department: ShortDepartment = None,
            order_by: AbnormalCheckingOrderBy = AbnormalCheckingOrderBy.in_time,
            order_direction: OrderDirection = OrderDirection.asc,
    ):
        query = self.db.query(AbnormalChecking)

        if start_time:
            query = query.filter(AbnormalChecking.out_time >= start_time)
        if end_time:
            query = query.filter(AbnormalChecking.in_time <= end_time)
        if floor_number:
            query = query.filter(AbnormalChecking.floor == floor_number)
        if search_query or department:
            query = query.join(Employee, Employee.id == AbnormalChecking.employee_id, isouter=False)

            if search_query:
                query = query.filter(or_(
                    AbnormalChecking.employee_id.ilike(f"%{search_query}%"),
                    Employee.first_name.ilike(f"%{search_query}%"),
                    Employee.last_name.ilike(f"%{search_query}%"),
                    (Employee.first_name + ' ' + Employee.last_name).ilike(f"%{search_query}%"),
                    (Employee.last_name + ' ' + Employee.first_name).ilike(f"%{search_query}%"),
                ))
            if department:
                query = query.filter(Employee.short_dept == department.value)

        return query.order_by(order_direction.to_orm_operator(order_by.value))

    def count_by_options(self, start_time: datetime = None, end_time: datetime = None, floor_number: int = None, search_query: str = None, department: str = None):
        return self.__general_query_builder(start_time, end_time, floor_number, search_query, department).count()
