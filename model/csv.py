from typing import List
from sqlalchemy import (
    Column,
    Integer,
    String,
    TIMESTAMP,
    DECIMAL,
    BINARY,
)

from pydantic import BaseModel
from datetime import datetime

from packages.db.database import Base as DBBase

class CSVFileTable(DBBase):
    __tablename__ = 'csvfile'
    filename = Column('filename', String(200), primary_key=True)
    create_time = Column('create_time', TIMESTAMP)
    bucket_name = Column('bucket_name', String(200))
    kamera_id = Column('kamera_id', Integer)

class CSVTable(DBBase):
    __tablename__ = 'csvtable'
    time = Column('time', TIMESTAMP, primary_key=True)
    raw_data = Column('raw_data', Integer)
    flag = Column('flag', Integer)
    kamera_id = Column('kamera_id', Integer)



class CSVFile(BaseModel):
    time: datetime
    raw_data: int
    flag: int

    class Config:
        orm_mode = True