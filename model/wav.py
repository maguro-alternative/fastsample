from typing import List
from sqlalchemy import (
    Column,
    Integer,
    String,
    TIMESTAMP,
    DECIMAL,
    BINARY,
)
from sqlalchemy.dialects.postgresql import BYTEA

from pydantic import BaseModel
from datetime import datetime

from packages.db.database import Base as DBBase

class WaveFileTable(DBBase):
    __tablename__ = 'wavefile'
    filename = Column('filename', String(200), primary_key=True)
    sampling_freq = Column('sampling_freq', DECIMAL)
    channel = Column('channel', Integer)
    sample_width = Column('sample_width', Integer)
    start_time = Column('start_time', TIMESTAMP)
    end_time = Column('end_time', TIMESTAMP)
    bucket_name = Column('bucket_name', String(200))
    kamera_id = Column('kamera_id', Integer, primary_key=True)

class WaveTable(DBBase):
    __tablename__ = 'wavetable'
    time = Column('time', TIMESTAMP, primary_key=True)
    frame_count = Column('frame_count', BYTEA)
    kamera_id = Column('kamera_id', Integer, primary_key=True)

class WaveFile(BaseModel):
    filename: str
    sampling_freq: float
    channel: int
    sample_width: int
    start_time: datetime
    end_time: datetime
    bucket_name: str
    kamera_id: int

    class Config:
        orm_mode = True

class Wave(BaseModel):
    time: datetime
    frame_count: List[bytes]
    kamera_id: int

    class Config:
        orm_mode = True

class ReadWaveFile(BaseModel):
    filename: str
    sampling_freq: float
    channel: int
    sample_width: int
    frames: int
    create_time: datetime
    wav_buffer16: bytes