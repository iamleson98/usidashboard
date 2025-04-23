from sqlalchemy.orm import Session, lazyload
from fastapi import Depends
from configs.db import get_db_connection

class BaseRepo:
    db: Session

    def __init__(self, db: Session = Depends(get_db_connection)):
        self.db = db
