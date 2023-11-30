from fastapi import APIRouter, File, UploadFile, Form, Depends
from sqlalchemy.orm import Session

import os
import shutil
from pathlib import Path
from tempfile import NamedTemporaryFile

from controllers.csv.csv_read import async_csv_read
from model.csv import CSVFileTable, CSVTable

from packages.db.database import get_db
from packages.gcs.gcs import GCSWrapper

from model.envconfig import EnvConfig

env = EnvConfig()

router = APIRouter()

@router.post("/save-upload-file/csv/")
async def save_upload_file_tmp(
    fileb: UploadFile=File(...),
    #token:str=Form(...),
    db: Session = Depends(get_db)
):
    tmp_path:Path = ""
    gcs_path = os.path.basename(fileb.filename)
    GCS = GCSWrapper(bucket_id=env.BUCKET_NAME)
    try:
        print(type(fileb))# <class 'starlette.datastructures.UploadFile'>
        print(type(fileb.file)) #<class 'tempfile.SpooledTemporaryFile'>
        suffix = Path(fileb.filename).suffix
        print(fileb.filename)
        with NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            shutil.copyfileobj(fileb.file, tmp)
            tmp_path = Path(tmp.name)
            print(tmp_path)

        GCS.upload_file(
            local_path=tmp_path.as_posix(),
            gcs_path=gcs_path
        )

        csv_list = await async_csv_read(
            filepath=tmp_path.as_posix(),
            filename=os.path.basename(fileb.filename)
        )

        db.add(CSVFileTable(
            filename=gcs_path,
            create_time=csv_list[0].time,
            bucket_name=env.BUCKET_NAME
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

@router.post("/save-upload-file/csv-timestamp/")
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
        with NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            shutil.copyfileobj(fileb.file, tmp)
            tmp_path = Path(tmp.name)
            print(tmp_path)

        csv_list = await async_csv_read(
            filepath=tmp_path.as_posix(),
            filename=os.path.basename(fileb.filename)
        )

        for csv_data in csv_list:
            db.add(CSVTable(
                time=csv_data.time,
                raw_data=csv_data.raw_data,
                flag=csv_data.flag
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