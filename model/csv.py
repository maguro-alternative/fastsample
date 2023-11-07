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
    time = Column('time', TIMESTAMP, primary_key=True)
    raw_data = Column('raw_data', Integer)
    flag = Column('flag', Integer)

class CSVFile(BaseModel):
    time: datetime
    raw_data: int
    flag: int

    class Config:
        orm_mode = True