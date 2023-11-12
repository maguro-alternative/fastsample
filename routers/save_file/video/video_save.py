from fastapi import APIRouter, File, UploadFile, Form, Depends
from sqlalchemy.orm import Session

import re
from datetime import datetime
import shutil
from pathlib import Path
from tempfile import NamedTemporaryFile

from controllers.pic.pic_storage import BUCKET
from model.video import VideoFileTable

from packages.file_time.creation_time import creation_date
from packages.db.database import get_db

router = APIRouter()

@router.post("/save-upload-file/video/")
async def save_upload_file_tmp(
    fileb: UploadFile=File(...),
    #token:str=Form(...),
    db: Session = Depends(get_db)
):
    tmp_path:Path = ""
    try:
        print(type(fileb))# <class 'starlette.datastructures.UploadFile'>
        print(type(fileb.file)) #<class 'tempfile.SpooledTemporaryFile'>
        suffix = Path(fileb.filename).suffix
        print(fileb.filename)
        create_time_str = fileb.filename.replace("log_", "")
        create_time_str = create_time_str.replace(".h264", "")
        record_time = re.match(r'\d{8}', create_time_str)
        if record_time is None:
            create_time = datetime.fromtimestamp(creation_date(create_time_str))
        else:
            create_time = datetime.strptime(record_time.group(), '%Y%m%d_%H%M%S')
        with NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            shutil.copyfileobj(fileb.file, tmp)
            tmp_path = Path(tmp.name)
            print(tmp_path)

        blob = BUCKET.blob(
            blob_name=tmp_path.as_posix()
        )
        blob.upload_from_filename(
            filename=tmp_path.as_posix()
        )

        db.add(VideoFileTable(
            filename=fileb.filename,
            create_time=create_time,
            bucket_name=BUCKET.name
        ))
        db.commit()
    finally:
        fileb.file.close()
    return {
        "filename": fileb.filename,
        "temporary_filepath": tmp_path,
        #"token": token,
        "fileb_content_type": fileb.content_type,
    }