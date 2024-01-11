from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_

from pathlib import Path
from typing import List
from datetime import datetime

from controllers.zip.zip_create import zipfiles
from controllers.csv.csv_read import async_csv_create
from model.csv import CSVFileTable,CSVTable

from model.envconfig import EnvConfig

from packages.db.database import get_db
from packages.gcs.gcs import GCSWrapper

env = EnvConfig()

router = APIRouter()
"""
http://localhost:5000/download-file/csv/?start_time=2023-10-18%2012:00:00&end_time=2023-10-18%2012:00:10
"""
@router.get("/download-file/csv/")
async def download_file_tmp(
    start_time:str,
    end_time:str,
    kamera_id: int = ...,
    db: Session = Depends(get_db)
):
    before_time = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
    after_time = datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S')
    print(before_time, after_time)

    csv_file_data:List[CSVFileTable] = db.query(CSVFileTable).filter(
        and_(
            CSVFileTable.create_time.between(
                before_time,
                after_time
            ),
            CSVFileTable.kamera_id == kamera_id
        )
    ).all()

    file_path_list = list()
    file_name_list = list()
    GCS = GCSWrapper(bucket_id=env.BUCKET_NAME)

    for csv_file in csv_file_data:
        suffix = Path(csv_file.filename).suffix
        GCS.download_file(
            local_path=suffix,
            gcs_path=csv_file.filename
        )
        file_path_list.append(suffix)
        file_name_list.append(csv_file.filename)

    if len(file_path_list) == 0:
        return {
            "message": "No file"
        }
    elif len(file_path_list) == 1:
        return FileResponse(
            path=file_path_list[0],
            filename=file_name_list[0],
            media_type='text/csv'
        )
    else:
        return zipfiles(file_path_list)


@router.get("/download-file/csv-timestamp/")
async def download_file_tmp(
    start_time:str,
    end_time:str,
    kamera_id: int = ...,
    db: Session = Depends(get_db)
):
    before_time = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
    after_time = datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S')
    print(before_time, after_time)

    csv_data:List[CSVTable] = db.query(CSVTable).filter(
        and_(
            CSVTable.time.between(
                before_time,
                after_time
            ),
            CSVTable.kamera_id == kamera_id
        )
    ).all()

    await async_csv_create(csv_data, "/tmp/csv_data.csv")

    return FileResponse(
        path='/tmp/csv_data.csv',
        filename='csv_data.csv',
        media_type='text/csv'
    )