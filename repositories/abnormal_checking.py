# from models.employee import Employee
from repositories.base import BaseRepo
# from dto.employee import EmployeeSearch
from datetime import datetime


class AbnormalCheckingRepo(BaseRepo):
    def list_by_conditions(self, limit: int = 100, offset: int = 0, start_time: datetime = None, end_time: datetime = None):
        pass
