from sqlalchemy.orm import Session, lazyload
from fastapi import Depends
from configs.db import get_db_connection
from typing import TypeVar, Generic, Optional
# from models.employee import Employee
import typing as tp

# Type definition for Model
M = TypeVar("M")

# Type definition for Unique Id
K = TypeVar("K")

class BaseRepo(Generic[M, K]):
    db: Session

    def __init__(self, db: Session = Depends(get_db_connection)):
        self.db = db

    def create(self, instance: M) -> M:
        self.db.add(instance)
        self.db.commit()
        self.db.refresh(instance)
        return instance
    
    def bulk_create(self, instances: tp.List[M]):
        self.db.bulk_save_objects(instances)
        self.db.commit()

    def delete(self, instance: M):
        self.db.delete(instance)
        self.db.commit()
        self.db.flush()

    def update(self, id: K, instance: M):
        instance.id = id
        self.db.merge(instance)
        self.db.commit()
        return instance

    def get_by_id(self, id: K, instance_cls: type) -> Optional[M]:
        return self.db.get(
            instance_cls,
            id,
        )
