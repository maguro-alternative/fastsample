from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

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
    db: Session = Depends(get_db)
):
    before_time = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
    after_time = datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S')
    print(before_time, after_time)

    csv_file_data:List[CSVFileTable] = db.query(CSVFileTable).filter(
        CSVFileTable.create_time.between(
            before_time,
            after_time
        )
    ).all()

    file_list = list()
    GCS = GCSWrapper(bucket_id=env.BUCKET_NAME)

    for csv_file in csv_file_data:
        GCS.download_file(
            local_path=f"/tmp/{csv_file.filename}",
            gcs_path=csv_file.filename
        )
        file_list.append(f"/tmp/{csv_file.filename}")

    if len(file_list) == 0:
        return {
            "message": "No file"
        }
    elif len(file_list) == 1:
        return FileResponse(
            path=file_list[0],
            filename=file_list[0],
            media_type='text/csv'
        )
    else:
        return zipfiles(file_list)


@router.get("/download-file/csv-timestamp/")
async def download_file_tmp(
    start_time:str,
    end_time:str,
    db: Session = Depends(get_db)
):
    before_time = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
    after_time = datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S')
    print(before_time, after_time)

    csv_data:List[CSVTable] = db.query(CSVTable).filter(
        CSVTable.time.between(
            before_time,
            after_time
        )
    ).all()

    await async_csv_create(csv_data, "/tmp/csv_data.csv")

    return FileResponse(
        path='/tmp/csv_data.csv',
        filename='csv_data.csv',
        media_type='text/csv'
    )