from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_

from typing import List
from datetime import datetime, timedelta

from packages.wav.wav_read import async_wave_create_bytes
from model.wav import WaveFileTable,WaveTable

from packages.db.database import get_db

router = APIRouter()
"""
http://localhost:5000/download-file/wav/?start_time=2023-11-04%2012:10:29&end_time=2023-11-04%2012:10:30
"""
@router.get("/download-file/wav/")
async def download_file_tmp(
    start_time:str,
    end_time:str,
    db: Session = Depends(get_db)
):
    before_time = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
    after_time = datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S')
    print(before_time, after_time)
    wav_data:List[WaveTable] = db.query(WaveTable).filter(
        WaveTable.time.between(
            before_time,
            after_time
        )
    ).all()
    wav_file_data:List[WaveFileTable] = db.query(WaveFileTable).filter(
        or_(
            and_(WaveFileTable.start_time <= before_time, before_time <= WaveFileTable.end_time),
            and_(WaveFileTable.start_time <= after_time, after_time <= WaveFileTable.end_time)
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
        out_file='./test.wav'
    )

    return FileResponse(
        path='./test.wav',
        filename='test.wav',
        media_type='audio/wav'
    )
