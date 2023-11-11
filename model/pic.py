from typing import List
from sqlalchemy import (
    Column,
    String,
    TIMESTAMP,
)

from pydantic import BaseModel
from datetime import datetime

from packages.db.database import Base as DBBase

class PICFileTable(DBBase):
    __tablename__ = 'picfile'
    filename = Column('filename', String(200), primary_key=True)
    create_time = Column('create_time', TIMESTAMP)
    bucket_name = Column('bucket_name', String(200))

class PICFile(BaseModel):
    filename: str
    create_time: datetime
    bucket_name: str

    class Config:
        orm_mode = True