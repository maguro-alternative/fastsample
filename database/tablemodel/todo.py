# $ python todo.py でテーブル作成
from sqlalchemy import (
    Boolean,
    Column,
    Integer,
    String,
    TIMESTAMP,
    DECIMAL,
    BOOLEAN,
    create_engine
)
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base


SQLALCHEMY_DATABASE_URI = "sqlite:///./test.db"
# SQLALCHEMY_DATABASE_URI = "postgresql://user:password@postgresserver/db"

ENGINE = create_engine(
    url=SQLALCHEMY_DATABASE_URI,
    connect_args={"check_same_thread": False},
    echo=True
)

Base = declarative_base()

class WaveTable(Base):
    __tabename__ = 'wavetable'
    time = Column('time', TIMESTAMP)
    sampling_freq = Column('sampling_freq', DECIMAL)
    channel = Column('channel', Integer)
    sample_width = Column('sample_width', Integer)
    frame_rate = Column('frame_rate', Integer)
    frame_count = Column('frame_count', Integer)

class CSVTabel(Base):
    __tablename__ = 'csvtable'
    time = Column('time', TIMESTAMP)
    infrared = Column('infrared', Integer)
    flag = Column('flag', Integer)

# テーブル作成
Base.metadata.create_all(bind=ENGINE)

# DB接続用のセッションクラス インスタンスが作成されると接続する
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)