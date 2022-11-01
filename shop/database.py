from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from functools import lru_cache
from . import config

@lru_cache()
def get_settings():
    return config.Settings()  # type: ignore

s = get_settings()
SQLALCHEMY_DATABASE_URL = f"postgresql://{s.db_user}:{s.db_pwd}@{s.db_host}/{s.db_name}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base() 
