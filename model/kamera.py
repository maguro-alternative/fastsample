from sqlalchemy import (
    Column,
    String,
    Integer
)

from packages.db.database import Base as DBBase

class KameraTable(DBBase):
    __tablename__ = 'kamera'
    id = Column('id', Integer, primary_key=True)
    address = Column('address', String(200), unique=True)