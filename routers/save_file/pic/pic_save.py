from fastapi import APIRouter, File, UploadFile, Form, Depends
from sqlalchemy.orm import Session

import os
import re
from datetime import datetime
import shutil
from pathlib import Path
from tempfile import NamedTemporaryFile

from model.pic import PICFileTable
from model.kamera import KameraTable

from packages.file_time.creation_time import creation_date
from packages.db.database import get_db
from packages.gcs.gcs import GCSWrapper

from model.envconfig import EnvConfig

env = EnvConfig()

router = APIRouter()

@router.post("/save-upload-file/pic/")
async def save_upload_file_tmp(
    fileb: UploadFile=File(...),
    address: str = Form,
    db: Session = Depends(get_db)
):
    """
    画像ファイルをGCSにアップロードし、DBに保存する

    fileb: UploadFile
        アップロードされたファイル
    address: str
        カメラのipアドレス
    """
    tmp_path:Path = ""
    gcs_path = os.path.basename(fileb.filename)
    GCS = GCSWrapper(bucket_id=env.BUCKET_NAME)
    try:
        suffix = Path(fileb.filename).suffix
        # ファイル名から作成日時を取得
        create_time_str = gcs_path.replace("log_", "")
        create_time_str = create_time_str.replace(".jpg", "")
        # 20211001_120000 の形式
        record_time = re.match(r'\d{8}_\d{6}', create_time_str)
        # 一時ファイルを作成
        with NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            shutil.copyfileobj(fileb.file, tmp)
            tmp_path = Path(tmp.name)
            print(tmp_path)

        # 時刻が取得できなかった場合はファイルの作成日時を取得
        if record_time is None:
            create_time = datetime.fromtimestamp(creation_date(tmp_path.as_posix()))
        else:
            create_time = datetime.strptime(record_time.group(), '%Y%m%d_%H%M%S')

        # 一時ファイルをGCSにアップロード
        GCS.upload_file(
            local_path=tmp_path.as_posix(),
            gcs_path=gcs_path
        )

        # ipアドレスからカメラのidを取得
        kamera_id:int = db.query(KameraTable.id).filter(
            KameraTable.address == address
        ).first().id

        # 画像ファイルのデータをDBに保存
        db.add(PICFileTable(
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