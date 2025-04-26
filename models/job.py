from models.base import EntityMeta
import sqlalchemy as sq


class Job(EntityMeta):
    __tablename__ = "jobs"

    id = sq.Column(sq.BigInteger, primary_key=True, autoincrement=True)
    job_type = sq.Column(sq.String(100), nullable=False)
    execution_at = sq.Column(sq.DateTime)
    status = sq.Column(sq.Boolean)
    reason = sq.Column(sq.String(1000))
