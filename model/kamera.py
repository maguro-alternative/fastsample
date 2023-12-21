from sqlalchemy import (
    Column,
    String,
    TIMESTAMP,
    Integer
)

from pydantic import BaseModel
from datetime import datetime

from packages.db.database import Base as DBBase

class KameraTable(DBBase):
    __tablename__ = 'kamera'
    id = Column('id', Integer, primary_key=True)
    address = Column('address', String(200), unique=True)