from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from typing import List,Dict
from datetime import datetime

from model.csv import CSVFileTable

from packages.db.database import get_db

router = APIRouter()
"""
http://localhost:5000/download-file/csv/?start_time=2023-10-18%2012:00:00&end_time=2023-10-18%2012:00:10
"""
@router.get("/view/csv/")
async def download_file_tmp(
    start_time:str='1970-01-01 00:00:00',
    end_time:str='2038-01-19 03:14:08',
    db: Session = Depends(get_db)
):
    before_time = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
    after_time = datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S')
    print(before_time, after_time)

    csv_data:List[CSVFileTable] = db.query(CSVFileTable).filter(
        CSVFileTable.time.between(
            before_time,
            after_time
        )
    ).all()

    csv_data_list:List[Dict] = [
        {
            "time":csv.time,
            "raw_data":csv.raw_data,
            "flag":csv.flag
        } for csv in csv_data
    ]

    return csv_data_list