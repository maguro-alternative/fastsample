from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_

from typing import List
from datetime import datetime, timedelta

from controllers.pic.pic_storage import BUCKET
from controllers.zip.zip_create import zipfiles
from model.video import VideoFileTable

from packages.db.database import get_db

router = APIRouter()


@router.get("/download-file/video/")
async def download_file_tmp(
    start_time:str,
    end_time:str,
    db: Session = Depends(get_db)
):
    before_time = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
    after_time = datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S')
    print(before_time, after_time)
    pic_file_data:List[VideoFileTable] = db.query(VideoFileTable).filter(
        and_(
            VideoFileTable.create_time >= before_time,
            after_time >= VideoFileTable.create_time
        )
    ).all()

    file_list = list()

    for pic_file in pic_file_data:
        blob = BUCKET.blob(
            blob_name=pic_file.filename
        )
        blob.download_to_filename(
            filename=f"./{pic_file.filename}"
        )
        file_list.append(f"./{pic_file.filename}")

    if len(file_list) == 0:
        return {
            "message": "No file"
        }
    elif len(file_list) == 1:
        return FileResponse(
            path=file_list[0],
            filename=file_list[0],
            media_type='video/mp4'
        )

    return zipfiles(file_list, "pic_data.zip")