from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from typing import List
from datetime import datetime, timedelta

from packages.wav.wav_read import async_wave_create_bytes
from model.wav import WaveFileTable,WaveTable

from packages.db.database import get_db

router = APIRouter()
"""
$ curl -X POST "http://localhost:8000/saveuploadfile/wav/" -H  "accept: application/json" -H  "Content-Type: multipart/form-data" -F "token=agd" -F "fileb=@toujyo.wav;type=audio/wav"

$ curl -X POST
    "http://127.0.0.1:8000/saveuploadfile/"
    -H  "accept: application/json" -H
    "Content-Type: multipart/form-data"
    -F "token=agd"
    -F "fileb=@archive.zip;type=application/x-zip-compressed"
"""
@router.get("/download-file/wav/")
async def download_file_tmp(
    start_time:str,
    end_time:str,
    db: Session = Depends(get_db)
):
    before_time = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
    after_time = datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S')
    wav_data:List[WaveTable] = db.query(WaveTable).filter(
        WaveTable.time.between(
            before_time,
            after_time
        )
    ).all()
    wav_file_data:List[WaveFileTable] = db.query(WaveFileTable).filter(
        WaveFileTable.start_time.between(
            before_time,
            after_time
        )
    ).all()
    byte = b''
    for data in wav_data:
        byte += data.frame_count

    await async_wave_create_bytes(
        data=byte,
        sampling_freq=wav_file_data[0].sampling_freq,
        channel=wav_file_data[0].channel,
        sample_width=wav_file_data[0].sample_width,
        out_file='./data/test.wav'
    )

    return FileResponse(
        path='./data/test.wav',
        filename='test.wav',
        media_type='audio/wav'
    )
