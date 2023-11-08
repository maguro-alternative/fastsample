from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_

from typing import List
from datetime import datetime, timedelta

from packages.csv.csv_read import csv_create
from model.csv import CSVFileTable,CSVFile

from packages.db.database import get_db

router = APIRouter()
"""
http://localhost:5000/download-file/wav/?start_time=2023-11-04%2012:10:29&end_time=2023-11-04%2012:10:30
"""
@router.get("/download-file/csv/")
async def download_file_tmp(
    start_time:str,
    end_time:str,
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

    csv_create(csv_data, "csv_data.csv")

    return FileResponse(
        path='./csv_data.csv',
        filename='csv_data.csv',
        media_type='text/csv'
    )