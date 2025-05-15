from enum import Enum
from pydantic import BaseModel

class SettingType(Enum):
    data_crawler = "data_crawler"


class SettingKey(Enum):
    run_data_crawler = "run_data_crawler"


class SettingValue(Enum):
    disable_data_crawler = "disable"
    enable_data_crawler = "enable"


class SettingSchema(BaseModel):
    id: int
    setting_type: SettingType
    key: SettingKey
    value: SettingValue

