from fastapi import APIRouter, File, UploadFile, Form
import shutil
from pathlib import Path
from tempfile import NamedTemporaryFile

from packages.wav.wav_read import async_wav_read
from model.wav import WaveFileTable,WaveTable

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
async def save_upload_file_tmp(fileb: UploadFile=File(...), token:str=Form(...)):
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
    finally:
        fileb.file.close()
    return {
        "filename": fileb.filename,
        "temporary_filepath": tmp_path,
        "token": token,
        "fileb_content_type": fileb.content_type,
    }