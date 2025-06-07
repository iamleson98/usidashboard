from repositories.checkout_events import CheckingEventRepo
from fastapi import Depends
from models.checking_event import CheckingEvent
import typing as tp
from services.base import BaseService


class CheckingEventService(BaseService):
    checkoutRepo: CheckingEventRepo

    def __init__(self, checkoutRepo: CheckingEventRepo = Depends()):
        self.checkoutRepo = checkoutRepo
        super().__init__()

    def find_checking_events_by_employee(self, employee_id: str, offset: int = 0, limit: int = 100) -> tp.List[CheckingEvent]:
        return self.checkoutRepo.find_by_employee_id(employee_id, offset, limit)
    