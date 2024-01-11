from fastapi import APIRouter, Depends, Form
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_

from pathlib import Path
from typing import List
from datetime import datetime

from controllers.zip.zip_create import zipfiles
from model.pic import PICFileTable
from packages.gcs.gcs import GCSWrapper

from model.envconfig import EnvConfig

from packages.db.database import get_db
from packages.gcs.gcs import GCSWrapper

env = EnvConfig()

router = APIRouter()

"""
http://localhost:5000/download-file/pic/?start_time=2023-10-25%205:59:00&end_time=2023-10-25%206:01:00
"""
@router.get("/download-file/pic/")
async def download_file_tmp(
    start_time:str,
    end_time:str,
    kamera_id: int = Form(...),
    db: Session = Depends(get_db)
):
    before_time = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
    after_time = datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S')
    print(before_time, after_time)
    pic_file_data:List[PICFileTable] = db.query(PICFileTable).filter(
        and_(
            PICFileTable.create_time >= before_time,
            after_time >= PICFileTable.create_time,
            PICFileTable.kamera_id == kamera_id
        )
    ).all()

    file_path_list = list()
    file_name_list = list()
    GCS = GCSWrapper(bucket_id=env.BUCKET_NAME)

    for pic_file in pic_file_data:
        suffix = Path(pic_file.filename).suffix
        GCS.download_file(
            local_path=suffix,
            gcs_path=pic_file.filename
        )
        file_path_list.append(suffix)
        file_name_list.append(pic_file.filename)

    if len(file_path_list) == 0:
        return {
            "message": "No file"
        }
    elif len(file_path_list) == 1:
        return FileResponse(
            path=file_path_list[0],
            filename=file_name_list[0],
            media_type='image/jpeg'
        )

    return zipfiles(file_path_list, "pic_data.zip")