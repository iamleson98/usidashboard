from enum import Enum
from sqlalchemy import asc, desc
from pydantic import BaseModel
import typing as tp

class OrderDirection(Enum):
    desc = "descending"
    asc = "ascending"

    @property
    def to_orm_operator(self):
        return asc if self == self.asc else desc


T = tp.TypeVar('T')


class ListReturnSchema(BaseModel, tp.Generic[T]):
    total: int
    error: str | None = None
    status: int
    records: list[T] | None = None


class SingleReturnSchema(BaseModel, tp.Generic[T]):
    error: str | None = None
    status: int
    record: T | None = None
