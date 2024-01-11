from fastapi import APIRouter, File, UploadFile, Depends, Body, Form
from sqlalchemy.orm import Session
import numpy as np

import os
import shutil
from pathlib import Path
from tempfile import NamedTemporaryFile
from datetime import timedelta

from controllers.wav.wav_read import async_wav_read
from model.wav import WaveFileTable,WaveTable
from model.kamera import KameraTable, KameraAddress

from packages.db.database import get_db
from packages.gcs.gcs import GCSWrapper

from model.envconfig import EnvConfig

env = EnvConfig()

router = APIRouter()
"""
$ curl -X POST "http://localhost:8000/saveuploadfile/wav/" -H  "accept: application/json" -H  "Content-Type: multipart/form-data" -F "token=agd" -F "fileb=@fastsample/test/data/toujyo.wav;type=audio/wav"

Invoke-RestMethod -Uri "http://localhost:5000/save-upload-file/wav/" -Method Post -Headers @{"accept" = "application/json"} -ContentType "multipart/form-data" -Body @{
    token="agd";
    fileb=(Get-Item ".\fastsample\test\data\toujyo.wav")
}


$ curl -X POST
    "http://127.0.0.1:8000/saveuploadfile/"
    -H  "accept: application/json" -H
    "Content-Type: multipart/form-data"
    -F "token=agd"
    -F "fileb=@archive.zip;type=application/x-zip-compressed"
"""
@router.post("/save-upload-file/wav/")
async def save_upload_file_tmp(
    fileb: UploadFile=File(...),
    db: Session = Depends(get_db),
    address: str = Form(...)
):
    print(address)
    tmp_path:Path = ""
    gcs_path = os.path.basename(fileb.filename)
    GCS = GCSWrapper(bucket_id=env.BUCKET_NAME)
    try:
        suffix = Path(fileb.filename).suffix
        with NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            shutil.copyfileobj(fileb.file, tmp)
            tmp_path = Path(tmp.name)
            print(tmp_path)

        # 一時ファイルをGCSにアップロード
        GCS.upload_file(
            local_path=tmp_path.as_posix(),
            gcs_path=gcs_path
        )

        # wavファイルを読み込み
        wav_file = await async_wav_read(
            filepath=tmp_path.as_posix(),
            filename=os.path.basename(fileb.filename)
        )
        # ipアドレスからカメラIDを取得
        kamera_id:int = db.query(KameraTable).filter(
            KameraTable.address == address
        ).first().id

        db.add(WaveFileTable(
            filename=gcs_path,
            sampling_freq=wav_file.sampling_freq,
            channel=wav_file.channel,
            sample_width=wav_file.sample_width,
            start_time=wav_file.create_time,
            end_time=wav_file.create_time + timedelta(microseconds=1.0/wav_file.sampling_freq*wav_file.frames*1000000),
            kamera_id=kamera_id
        ))

        print(wav_file.create_time)

        db.commit()
    finally:
        fileb.file.close()
    return {
        "filename": fileb.filename,
        "temporary_filepath": tmp_path,
        "start_time": wav_file.create_time,
        "end_time": wav_file.create_time + timedelta(microseconds=1.0/wav_file.sampling_freq*wav_file.frames*1000000),
        "fileb_content_type": fileb.content_type,
    }

@router.post("/save-upload-file/wav-timestamp/")
async def save_upload_file_tmp(
    fileb: UploadFile=File(...),
    address: str = Form(...),
    db: Session = Depends(get_db)
):
    tmp_path:Path = ""
    try:
        # 一時ファイルを作成
        suffix = Path(fileb.filename).suffix
        with NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            shutil.copyfileobj(fileb.file, tmp)
            tmp_path = Path(tmp.name)
            print(tmp_path)

        # wavファイルを読み込み
        wav_file = await async_wav_read(
            filepath=tmp_path.as_posix(),
            filename=os.path.basename(fileb.filename)
        )

        # ipアドレスからカメラIDを取得
        kamera_id:int = db.query(KameraTable).filter(
            KameraTable.address == address
        ).first().id

        db.add(WaveFileTable(
            filename=wav_file.filename,
            sampling_freq=wav_file.sampling_freq,
            channel=wav_file.channel,
            sample_width=wav_file.sample_width,
            start_time=wav_file.create_time,
            end_time=wav_file.create_time + timedelta(microseconds=1.0/wav_file.sampling_freq*wav_file.frames*1000000),
            kamera_id=kamera_id
        ))

        print(wav_file.create_time)

        # wavファイルのバイナリを展開
        wav_buffer16:np.ndarray[np.int16] = np.frombuffer(wav_file.wav_buffer16, dtype=np.int16)
        for rate in wav_buffer16:
            # 1フレーム分の時間を追加
            wav_file.create_time += timedelta(microseconds=1.0/wav_file.sampling_freq*1000000)
            # wavファイルのデータをDBに保存
            db.add(WaveTable(
                time=wav_file.create_time,
                frame_count=rate
            ))

        db.commit()
    finally:
        fileb.file.close()
    return {
        "filename": fileb.filename,
        "temporary_filepath": tmp_path,
        "start_time": wav_file.create_time,
        "end_time": wav_file.create_time + timedelta(microseconds=1.0/wav_file.sampling_freq*wav_file.frames*1000000),
        "fileb_content_type": fileb.content_type,
    }