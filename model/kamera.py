from sqlalchemy import (
    Column,
    String,
    Integer
)

from pydantic import BaseModel

from packages.db.database import Base as DBBase
# DROP TABLE wavefile, wavetable, csvfile, csvtable, picfile, videofile;
class KameraTable(DBBase):
    __tablename__ = 'kamera'
    id = Column('id', Integer, primary_key=True)
    address = Column('address', String(200), unique=True)

class Kamera(BaseModel):
    id: int
    address: str

    class Config:
        orm_mode = True

class KameraAddress(BaseModel):
    address: str

    class Config:
        orm_mode = True