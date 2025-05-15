from repositories.base import BaseRepo
from models.job import Job, Setting
import sqlalchemy as sq
from dto.settings import SettingValue, SettingKey, SettingType

class JobRepo(BaseRepo):
    def get_last_job(self, only_success: bool = False):
        """returns the most recent job"""
        query = self.db.query(Job)

        if only_success:
            query = query.filter(Job.status == True)

        return query.order_by(sq.desc(Job.execution_at)).first()


class SettingRepo(BaseRepo):
    def get_by_type(self, setting_type: SettingType, key: SettingKey = None):
        query = self.db.query(Setting).filter(Setting.setting_type == setting_type)
        if key:
            query = query.filter(Setting.key == key)

        return query.first()

    def update_by_type_and_key(self, setting_type: SettingType, key: SettingKey, value: SettingValue) -> Setting:
        setting = self.get_by_type(setting_type, key)
        if setting:
            setting.value = value
        else:
            new_setting = Setting(
                setting_type=setting_type,
                key=key,
                value=value,
            )
            return self.create(new_setting)

        return self.update(setting.id, setting)

