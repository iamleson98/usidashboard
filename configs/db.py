from configs.env import get_environment_variables
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

env = get_environment_variables()

DATABASE_URL = f"mysql://{env.DB_USERNAME}:{env.DB_PASSWORD}@{env.DB_HOST}:{env.DB_PORT}/{env.DB_NAME}"

Engine = create_engine(
    DATABASE_URL, echo=env.DEBUG_MODE, future=True
)

SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=Engine
)

def get_db_connection():
    db = scoped_session(SessionLocal)
    try:
        yield db
    finally:
        db.close()
