from sqlalchemy.orm import Session
from fastapi import Depends
from configs.db import get_db_connection
from typing import TypeVar, Generic, Optional
import typing as tp
from sqlalchemy import update

# Type definition for Model
M = TypeVar("M")

# Type definition for Unique Id
K = TypeVar("K")

class BaseRepo(Generic[M, K]):
    def __init__(self, db: Session = Depends(get_db_connection)):
        self.db = db

    def create(self, instance: M) -> M | None:
        try:
            self.db.add(instance)
            self.db.commit()
            self.db.refresh(instance)
            return instance
        except Exception:
            self.db.rollback()
            return None
    
    def bulk_create(self, instances: tp.List[M]) -> bool:
        try:
            self.db.bulk_save_objects(instances)
            self.db.commit()
            return True
        except Exception:
            self.db.rollback()
            return False

    def delete(self, instance: M) -> bool:
        try:
            self.db.delete(instance)
            self.db.commit()
            self.db.flush()
            return True
        except Exception:
            self.db.rollback()
            return False

    def update(self, id: K, instance: M) -> M | None:
        try:
            instance.id = id
            self.db.merge(instance)
            self.db.commit()
            # self.db.expire_all()
            return instance
        except Exception as e:
            self.db.rollback()
            return None

    def get_by_id(self, id: K, instance_cls: type) -> Optional[M]:
        return self.db.get(
            instance_cls,
            id,
        )
