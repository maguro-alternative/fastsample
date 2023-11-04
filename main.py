import uvicorn
from fastapi import FastAPI,Depends

import os

from dotenv import load_dotenv
load_dotenv()
from routers import (
    index
)
from routers.api import (
    test_success
)

from packages.db.database import ENGINE, DBBase

DBBase.metadata.create_all(bind=ENGINE)


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

# フォーム送信テスト用
app.include_router(router=test_success.router)

# ローカル実行
def local_run():
    # reloadでホットリロードを有効
    # "ファイル名:FastAPIのインスタンス名"で定義
    uvicorn.run(
        app=app,
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
        run()