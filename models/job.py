from models.base import EntityMeta
import sqlalchemy as sq
from dto.settings import SettingSchema

class Job(EntityMeta):
    __tablename__ = "jobs"

    id = sq.Column(sq.BigInteger, primary_key=True, autoincrement=True)
    job_type = sq.Column(sq.String(100), nullable=False)
    execution_at = sq.Column(sq.DateTime)
    status = sq.Column(sq.Boolean)
    reason = sq.Column(sq.String(1000))


class Setting(EntityMeta):
    __tablename__ = "settings"

    id = sq.Column(sq.BigInteger, primary_key=True, autoincrement=True)
    setting_type = sq.Column(sq.String(50), nullable=False)
    key = sq.Column(sq.String(50), nullable=False)
    value = sq.Column(sq.String(50), nullable=False)

    def normalize(self):
        """normalize returns basic information of an employee"""
        return SettingSchema(
            id=self.id,
            setting_type=self.setting_type,
            key=self.key,
            value=self.value,
        )
