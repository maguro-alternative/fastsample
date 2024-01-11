from fastapi import APIRouter, File, UploadFile, Form, Depends
from sqlalchemy.orm import Session

import os
import re
from datetime import datetime
import shutil
from pathlib import Path
from tempfile import NamedTemporaryFile

from model.video import VideoFileTable
from model.kamera import KameraTable

from packages.file_time.creation_time import creation_date
from packages.db.database import get_db
from packages.gcs.gcs import GCSWrapper

from model.envconfig import EnvConfig

env = EnvConfig()

router = APIRouter()

@router.post("/save-upload-file/video/")
async def save_upload_file_tmp(
    fileb: UploadFile=File(...),
    kamera_address: int = ...,
    db: Session = Depends(get_db)
):
    tmp_path:Path = ""
    gcs_path = os.path.basename(fileb.filename)
    GCS = GCSWrapper(bucket_id=env.BUCKET_NAME)
    try:
        suffix = Path(fileb.filename).suffix
        # ファイル名から作成日時を取得
        create_time_str = gcs_path.replace("log_", "")
        create_time_str = create_time_str.replace(".h264", "")
        record_time = re.match(r'\d{8}_\d{6}', create_time_str)
        # 時刻が取得できなかった場合はファイルの作成日時を取得
        if record_time is None:
            create_time = datetime.fromtimestamp(creation_date(gcs_path))
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

        kamera_id:int = db.query(KameraTable.id).filter(
            KameraTable.address == kamera_address
        ).first().id

        # csvファイルのデータをDBに保存
        db.add(VideoFileTable(
            filename=gcs_path,
            create_time=create_time,
            bucket_name=env.BUCKET_NAME,
            kamera_id=kamera_id
        ))
        db.commit()
    finally:
        fileb.file.close()
    return {
        "filename": gcs_path,
        "temporary_filepath": tmp_path,
        "fileb_content_type": fileb.content_type,
    }