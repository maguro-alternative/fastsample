from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_

from pathlib import Path
from typing import List
from datetime import datetime

from controllers.zip.zip_create import zipfiles
from controllers.wav.wav_read import async_wave_create_bytes
from model.wav import WaveFileTable,WaveTable

from model.envconfig import EnvConfig

from packages.db.database import get_db
from packages.gcs.gcs import GCSWrapper

env = EnvConfig()

router = APIRouter()
"""
http://localhost:5000/download-file/wav/?start_time=2023-11-04%2012:10:29&end_time=2023-11-04%2012:10:30
http://localhost:5000/download-file/wav/?start_time=2023-11-11%2016:14:11&end_time=2023-11-11%2016:14:13
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
    # 指定した時間のwavデータを取得
    wav_file_data:List[WaveFileTable] = db.query(WaveFileTable).filter(
        or_(
            and_(WaveFileTable.start_time <= before_time, before_time <= WaveFileTable.end_time),
            and_(WaveFileTable.start_time <= after_time, after_time <= WaveFileTable.end_time)
        )
    ).all()

    file_path_list = list()
    file_name_list = list()
    # GCSのインスタンスを作成
    GCS = GCSWrapper(bucket_id=env.BUCKET_NAME)

    for wav_file in wav_file_data:
        # GCSからファイルをダウンロード
        suffix = Path(wav_file.filename).suffix
        GCS.download_file(
            local_path=suffix,
            gcs_path=wav_file.filename
        )
        file_path_list.append(suffix)
        file_name_list.append(wav_file.filename)

    if len(file_path_list) == 0:
        return {
            "message": "No file"
        }
    elif len(file_path_list) == 1:
        return FileResponse(
            path=file_path_list[0],
            filename=file_name_list[0],
            media_type='audio/wav'
        )

    return zipfiles(file_path_list, "pic_data.zip")

@router.get("/download-file/wav-timestamp/")
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
        # バイトデータを結合
        byte += data.frame_count

    # wavファイルを作成
    await async_wave_create_bytes(
        data=byte,
        sampling_freq=wav_file_data[0].sampling_freq,
        channel=wav_file_data[0].channel,
        sample_width=wav_file_data[0].sample_width,
        out_file='/tmp/test.wav'
    )

    return FileResponse(
        path='/tmp/test.wav',
        filename='test.wav',
        media_type='audio/wav'
    )