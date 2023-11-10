from sqlalchemy import (
    create_engine
)
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from model.envconfig import EnvConfig

env = EnvConfig()

#SQLALCHEMY_DATABASE_URI = "sqlite:///./sqlite/test.db"
SQLALCHEMY_DATABASE_URI = env.NODRIVER_DATABASE_URI

ENGINE = create_engine(
    url=SQLALCHEMY_DATABASE_URI,
    connect_args={"check_same_thread": False},
    echo=True
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=ENGINE)

Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()