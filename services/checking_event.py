from repositories.checkout_events import CheckoutEventRepo
from fastapi import Depends
from models.checking_event import CheckingEvent
import typing as tp

class CheckingEventService:
    checkoutRepo: CheckoutEventRepo

    def __init__(self, checkoutRepo: CheckoutEventRepo = Depends()):
        self.checkoutRepo = checkoutRepo

    def find_checking_events_by_employee(self, employee_id: str, offset: int = 0, limit: int = 100) -> tp.List[CheckingEvent]:
        return self.checkoutRepo.find_by_employee_id(employee_id, offset, limit)
