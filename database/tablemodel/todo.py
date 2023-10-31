# $ python todo.py でテーブル作成
from sqlalchemy import (
    Boolean,
    Column,
    Integer,
    String,
    TIMESTAMP,
    DECIMAL,
    create_engine
)
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base


SQLALCHEMY_DATABASE_URI = "sqlite:///./test.db"
# SQLALCHEMY_DATABASE_URI = "postgresql://user:password@postgresserver/db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URI,
    connect_args={"check_same_thread": False},
    echo=True
)

Base = declarative_base()

# Todoテーブルの定義
class Todo(Base):
    __tablename__ = 'todos'
    id = Column('id', Integer, primary_key = True)
    title = Column('title', String(200))
    done = Column('done', Boolean, default=False)

class WaveTable(Base):
    __tabename__ = 'wavetable'
    time = Column('time', TIMESTAMP, primary_key = True)
    sampling_freq = Column('sampling_freq', DECIMAL)
    channel = Column('channel', Integer)
    sample_width = Column('sample_width', Integer)
    frame_rate = Column('frame_rate', Integer)
    frame_count = Column('frame_count', Integer)

# テーブル作成
Base.metadata.create_all(bind=engine)

# DB接続用のセッションクラス インスタンスが作成されると接続する
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)