from fastapi import APIRouter, File, UploadFile, Form, Depends
from sqlalchemy.orm import Session
import numpy as np

import os
import shutil
from pathlib import Path
from tempfile import NamedTemporaryFile
from datetime import datetime, timedelta

from packages.wav.wav_read import async_wav_read
from model.wav import WaveFileTable,WaveTable

from packages.db.database import get_db

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

        wav_file = await async_wav_read(
            filepath=tmp_path.as_posix(),
            filename=os.path.basename(fileb.filename)
        )

        db.add(WaveFileTable(
            filename=wav_file.filename,
            sampling_freq=wav_file.sampling_freq,
            channel=wav_file.channel,
            sample_width=wav_file.sample_width,
            start_time=wav_file.create_time,
            end_time=wav_file.create_time + timedelta(microseconds=1.0/wav_file.sampling_freq*wav_file.frames*1000000)
        ))

        wav_buffer16:np.ndarray[np.int16] = np.frombuffer(wav_file.wav_buffer16, dtype=np.int16)
        for rate in wav_buffer16:
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
        #"token": token,
        "fileb_content_type": fileb.content_type,
    }