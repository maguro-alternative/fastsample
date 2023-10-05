from fastapi import APIRouter, WebSocketDisconnect
from fastapi.responses import JSONResponse
from starlette.requests import Request
from starlette.websockets import WebSocket

router = APIRouter()

# 接続中のクライアントを識別するためのIDを格納
clients = {}

@router.get('/')
async def test_post(
    request:Request
):
    return JSONResponse(
        status_code=200,
        content={
            'result':'Hello World'
        }
    )

# WebSockets用のエンドポイント
@router.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()
    # クライアントを識別するためのIDを取得
    key = ws.headers.get('sec-websocket-key')
    clients[key] = ws
    try:
        while True:
            # クライアントからメッセージを受信
            data = await ws.receive_text()
            # 接続中のクライアントそれぞれにメッセージを送信（ブロードキャスト）
            for client in clients.values():
                await client.send_text(f"ID: {key} | Message: {data}")
    except WebSocketDisconnect:
        await ws.close()
        # 接続が切れた場合、当該クライアントを削除する
        del clients[key]