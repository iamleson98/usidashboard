from repositories.base import BaseRepo
from fastapi import Depends
from typing import TypeVar, Generic, Optional
import typing as tp

# Type definition for Model
M = TypeVar("M")

# Type definition for Unique Id
K = TypeVar("K")

class BaseService(Generic[M, K]):
    baseRepo: BaseRepo

    def __init__(self, baseRepo: BaseRepo = Depends()):
        self.baseRepo = baseRepo

    def create(self, instance: M) -> M:
        return self.baseRepo.create(instance)
    
    def bulk_create(self, instances: tp.List[M]) -> bool:
        return self.baseRepo.bulk_create(instances)

    def delete(self, instance: M) -> bool:
        return self.baseRepo.delete(instance)

    def update(self, id: K, instance: M) -> M:
        return self.baseRepo.update(id, instance)

    def get_by_id(self, id: K, instance_cls: type) -> Optional[M]:
        return self.baseRepo.get_by_id(id, instance_cls)
