from fastapi import APIRouter, File, UploadFile, Form, Depends
from sqlalchemy.orm import Session

import os
import shutil
from pathlib import Path
from tempfile import NamedTemporaryFile

from controllers.csv.csv_read import async_csv_read
from model.csv import CSVFileTable, CSVTable
from model.kamera import KameraTable

from packages.db.database import get_db
from packages.gcs.gcs import GCSWrapper

from model.envconfig import EnvConfig

env = EnvConfig()

router = APIRouter()

@router.post("/save-upload-file/csv/")
async def save_upload_file_tmp(
    fileb: UploadFile=File(...),
    kamera_address: int = ...,
    db: Session = Depends(get_db)
):
    tmp_path:Path = ""
    gcs_path = os.path.basename(fileb.filename)
    GCS = GCSWrapper(bucket_id=env.BUCKET_NAME)
    try:
        # 一時ファイルを作成
        suffix = Path(fileb.filename).suffix
        with NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            shutil.copyfileobj(fileb.file, tmp)
            tmp_path = Path(tmp.name)
            # 一時ファイルのパスを表示
            print(tmp_path)

        # 一時ファイルをGCSにアップロード
        GCS.upload_file(
            local_path=tmp_path.as_posix(),
            gcs_path=gcs_path
        )

        # csvファイルを読み込み
        csv_list = await async_csv_read(
            filepath=tmp_path.as_posix(),
            filename=os.path.basename(fileb.filename)
        )

        kamera_id:int = db.query(KameraTable.id).filter(
            KameraTable.address == kamera_address
        ).first().id

        # csvファイルのデータをDBに保存
        db.add(CSVFileTable(
            filename=gcs_path,
            create_time=csv_list[0].time,
            bucket_name=env.BUCKET_NAME,
            kamera_id=kamera_id
        ))

        db.commit()
    finally:
        fileb.file.close()
    return {
        "filename": fileb.filename,
        "temporary_filepath": tmp_path,
        "fileb_content_type": fileb.content_type,
    }

@router.post("/save-upload-file/csv-timestamp/")
async def save_upload_file_tmp(
    fileb: UploadFile=File(...),
    kamera_address: int = ...,
    db: Session = Depends(get_db)
):
    tmp_path:Path = ""
    try:
        suffix = Path(fileb.filename).suffix
        with NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            shutil.copyfileobj(fileb.file, tmp)
            tmp_path = Path(tmp.name)
            print(tmp_path)

        csv_list = await async_csv_read(
            filepath=tmp_path.as_posix(),
            filename=os.path.basename(fileb.filename)
        )

        kamera_id:int = db.query(KameraTable.id).filter(
            KameraTable.address == kamera_address
        ).first().id

        for csv_data in csv_list:
            # csvファイルの中身を1行ずつDBに保存
            db.add(CSVTable(
                time=csv_data.time,
                raw_data=csv_data.raw_data,
                flag=csv_data.flag,
                kamera_id=kamera_id
            ))

        db.commit()
    finally:
        fileb.file.close()
    return {
        "filename": fileb.filename,
        "temporary_filepath": tmp_path,
        "fileb_content_type": fileb.content_type,
    }