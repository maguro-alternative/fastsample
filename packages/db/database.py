from sqlalchemy import (
    create_engine
)
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from model.envconfig import EnvConfig

env = EnvConfig()

# データベースのURI
#SQLALCHEMY_DATABASE_URI = "sqlite:///./sqlite/test.db"
SQLALCHEMY_DATABASE_URI = env.NODRIVER_DATABASE_URI

# データベースのエンジン
ENGINE = create_engine(
    url=SQLALCHEMY_DATABASE_URI,
    pool_pre_ping=True,
    pool_recycle=300,
    #connect_args={"check_same_thread": False},
    echo=True
)

# セッションの作成
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=ENGINE)

# ベースモデルの作成
Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()