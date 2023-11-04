from fastapi import APIRouter, File, UploadFile, Form, Depends
from sqlalchemy.orm import Session

import shutil
from pathlib import Path
from tempfile import NamedTemporaryFile
from datetime import datetime, timedelta

from packages.wav.wav_read import async_wav_read
from model.wav import WaveFileTable,WaveTable

from packages.db.database import get_db

router = APIRouter()
"""
$ curl -X POST "http://127.0.0.1:8000/saveuploadfile/" -H  "accept: application/json" -H  "Content-Type: multipart/form-data" -F "token=agd" -F "fileb=@archive.zip;type=application/x-zip-compressed"

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
    token:str=Form(...),
    db: Session = Depends(get_db)
):
    tmp_path:Path = ""
    try:
        print(type(fileb))# <class 'starlette.datastructures.UploadFile'>
        print(type(fileb.file)) #<class 'tempfile.SpooledTemporaryFile'>
        suffix = Path(fileb.filename).suffix
        with NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            shutil.copyfileobj(fileb.file, tmp)
            tmp_path = Path(tmp.name)
            print(tmp_path)

        wav_file = await async_wav_read(tmp_path)

        db.add(WaveFileTable(
            filename=wav_file.filename,
            sampling_freq=wav_file.sampling_freq,
            channel=wav_file.channel,
            sample_width=wav_file.sample_width,
            start_time=wav_file.create_time,
            end_time=wav_file.create_time + timedelta(microseconds=1.0/wav_file.sampling_freq*wav_file.frames*1000000)
        ))

        for rate in wav_file.wav_buffer16:
            wav_file.create_time += timedelta(microseconds=1.0/wav_file.sampling_freq*1000000)
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
        "token": token,
        "fileb_content_type": fileb.content_type,
    }