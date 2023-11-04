from sqlalchemy import (
    create_engine
)
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

SQLALCHEMY_DATABASE_URI = "sqlite:///./sqlite/test.db"

ENGINE = create_engine(
    url=SQLALCHEMY_DATABASE_URI,
    connect_args={"check_same_thread": False},
    echo=True
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=ENGINE)

DBBase = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()