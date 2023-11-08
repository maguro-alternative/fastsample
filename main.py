import uvicorn
from fastapi import FastAPI,Depends

import os

from dotenv import load_dotenv
load_dotenv()
from routers import (
    index
)
from routers.save_file.wav import wav_save
from routers.download_file.wav import wav_download
from routers.save_file.csv import csv_save
from routers.download_file.csv import csv_download

from routers.api import (
    test_success
)

from packages.db.database import ENGINE
from model.wav import DBBase as DBBaseWav
from model.csv import DBBase as DBBaseCSV

DBBaseWav.metadata.create_all(bind=ENGINE)
DBBaseCSV.metadata.create_all(bind=ENGINE)

app = FastAPI(
    docs_url=None,
    redoc_url=None,
    openapi_url=None,
    title='FastAPIのテスト',
    description='',
    version='0.9 beta'
)

# 各パス
app.include_router(router=index.router)

app.include_router(router=wav_save.router)
app.include_router(router=wav_download.router)
app.include_router(router=csv_save.router)
app.include_router(router=csv_download.router)

# フォーム送信テスト用
app.include_router(router=test_success.router)

# ローカル実行
def local_run():
    # reloadでホットリロードを有効
    # "ファイル名:FastAPIのインスタンス名"で定義
    uvicorn.run(
        app="main:app",
        host='localhost',
        port=int(os.getenv("PORT", default=5000)),
        reload=True,
        log_level="info"
    )

# 本番環境
def run():
    uvicorn.run(
        app="main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", default=8080)),
        reload=True,
        log_level="info"
    )

if __name__ == "__main__":
    # 環境変数にPORTSがない場合、ローカル環境での実行と判断
    if os.environ.get("PORTS") != None:
        local_run()
    # 本番環境として実行
    else:
        local_run()