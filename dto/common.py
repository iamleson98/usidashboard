from enum import Enum
from sqlalchemy import asc, desc

class OrderDirection(Enum):
    desc = "desc"
    asc = "asc"

    @property
    def to_orm_operator(self):
        return asc if self.value == self.asc else desc
