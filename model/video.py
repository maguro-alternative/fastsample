from typing import List
from sqlalchemy import (
    Column,
    String,
    TIMESTAMP,
    Integer
)

from pydantic import BaseModel
from datetime import datetime

from packages.db.database import Base as DBBase

class VideoFileTable(DBBase):
    __tablename__ = 'videofile'
    filename = Column('filename', String(200), primary_key=True)
    create_time = Column('create_time', TIMESTAMP)
    bucket_name = Column('bucket_name', String(200))
    kamera_id = Column('kamera_id', Integer)

class VideoFile(BaseModel):
    filename: str
    create_time: datetime
    bucket_name: str
    kamera_id: int

    class Config:
        orm_mode = True