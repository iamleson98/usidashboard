from pydantic import BaseModel
import typing as tp
from utils.custom_types import Error
import re

EMPLOYEE_ID_REGEX = re.compile(r"^(VN|TW|SH)\d{6}$")

class EmployeeSchema(BaseModel):
    """EmployeeSchema represents the structure of employee object"""
    id: str
    first_name: str
    last_name: str
    card_no: tp.Optional[str]
    is_visitor: tp.Optional[bool] = False
    department: tp.Optional[str]

    def is_valid(self) -> tp.Optional[Error]:
        match = EMPLOYEE_ID_REGEX.match(self.id)
        if not match:
            return Error(field="id", message="invalid id")
        if not self.first_name:
            return Error(field="first_name", message="Invalid first name")
        if not self.last_name:
            return Error(field="last_name", message="Invalid last name")

        return None


class EmployeeSearch(BaseModel):
    """EmployeeSearchOpts contains searching options for employees"""
    id: tp.Optional[str]
    first_name: tp.Optional[str]
    last_name: tp.Optional[str]
    limit: int
    offset: int
