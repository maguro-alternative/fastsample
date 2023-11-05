import re
import os
import platform
from datetime import datetime, timedelta

from sqlalchemy import (
    Boolean,
    Column,
    Integer,
    String,
    TIMESTAMP,
    DECIMAL,
    BOOLEAN,
    Float,
    create_engine
)
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base


FileName = './data/data_20231018_12.csv' # mono
SQLALCHEMY_DATABASE_URI = "sqlite:///./sqlite/test.db"

Base = declarative_base()

ENGINE = create_engine(
    url=SQLALCHEMY_DATABASE_URI,
    connect_args={"check_same_thread": False},
    echo=True
)

class CSVTabel(Base):
    __tablename__ = 'csvtable'
    filename = Column('filename', String(200), primary_key=True)
    start_time = Column('start_time', TIMESTAMP)
    end_time = Column('end_time', TIMESTAMP)

class CSVFileTable(Base):
    __tablename__ = 'csvfile'
    time = Column('time', TIMESTAMP, primary_key=True)
    raw_data = Column('raw_data', Integer)
    flag = Column('flag', Integer)

def creation_date(path_to_file:str) -> float:
    """
    Try to get the date that a file was created, falling back to when it was
    last modified if that isn't possible.
    See http://stackoverflow.com/a/39501288/1709587 for explanation.
    """
    if platform.system() == 'Windows':
        return os.path.getctime(path_to_file)
    else:
        stat = os.stat(path_to_file)
        try:
            return stat.st_birthtime
        except AttributeError:
            # We're probably on Linux. No easy way to get creation dates here,
            # so we'll settle for when its content was last modified.
            return stat.st_mtime

def csv_create_db(filepath:str,filename:str):
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=ENGINE)
    session = SessionLocal()
    filename = filename.replace("data_", "")
    filename = filename.replace(".csv", "")
    record_time = re.match(r'\d{8}', filename)
    if record_time is None:
        create_time = datetime.fromtimestamp(creation_date(filepath))
    else:
        create_time = datetime.strptime(record_time.group(), '%Y%m%d')

    create_time_str = create_time.strftime('%Y%m%d')

    with open(filepath, 'r') as f:
        data = f.readlines()
    for i, d in enumerate(data):
        time_str = create_time_str + d.split(',')[0]
        time = datetime.strptime(time_str, '%Y%m%d%H:%M:%S.%f')
        csv_table = CSVFileTable(**{
            "time":time,
            "raw_data":int(d.split(',')[1]),
            "flag":int(d.split(',')[2])
        })

        session.add(csv_table)

    session.commit()

def table_in():
    # テーブル作成
    Base.metadata.create_all(bind=ENGINE)

if __name__ == '__main__':
    table_in()
    csv_create_db(FileName,FileName)
