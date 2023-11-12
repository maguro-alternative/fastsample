from fastapi import APIRouter, File, UploadFile, Form, Depends
from sqlalchemy.orm import Session

import re
from datetime import datetime
import shutil
from pathlib import Path
from tempfile import NamedTemporaryFile

from model.pic import PICFileTable

from packages.file_time.creation_time import creation_date
from packages.db.database import get_db
from packages.gcs.gcs import GCSWrapper

from model.envconfig import EnvConfig

env = EnvConfig()

router = APIRouter()

@router.post("/save-upload-file/pic/")
async def save_upload_file_tmp(
    fileb: UploadFile=File(...),
    db: Session = Depends(get_db)
):
    tmp_path:Path = ""
    gcs_path = fileb.filename
    GCS = GCSWrapper(bucket_id=env.BUCKET_NAME)
    try:
        print(type(fileb))# <class 'starlette.datastructures.UploadFile'>
        print(type(fileb.file)) #<class 'tempfile.SpooledTemporaryFile'>
        suffix = Path(fileb.filename).suffix
        print(fileb.filename)
        create_time_str = fileb.filename.replace("log_", "")
        create_time_str = create_time_str.replace(".jpg", "")
        record_time = re.match(r'\d{8}', create_time_str)
        if record_time is None:
            create_time = datetime.fromtimestamp(creation_date(create_time_str))
        else:
            create_time = datetime.strptime(record_time.group(), '%Y%m%d_%H%M%S')
        with NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            shutil.copyfileobj(fileb.file, tmp)
            tmp_path = Path(tmp.name)
            print(tmp_path)

        GCS.upload_file(
            local_path=tmp_path.as_posix(),
            gcs_path=gcs_path
        )

        db.add(PICFileTable(
            filename=gcs_path,
            create_time=create_time,
            bucket_name=env.BUCKET_NAME
        ))
        db.commit()
    finally:
        fileb.file.close()
    return {
        "filename": gcs_path,
        "temporary_filepath": tmp_path,
        "fileb_content_type": fileb.content_type,
    }