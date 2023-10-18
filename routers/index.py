from fastapi import APIRouter, WebSocketDisconnect,Cookie, Depends, Header,Query,  status
from fastapi.responses import JSONResponse
from starlette.requests import Request
from starlette.websockets import WebSocket
import websockets

from typing import Optional,Dict

router = APIRouter()

# 接続中のクライアントを識別するためのIDを格納
clients:Dict[str, WebSocket] = {}

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

async def get_cookie_or_client(
    websocket: WebSocket,
    session: str = Cookie(None),
    x_client: str = Header(None)
):
    print(session)
    if session is None and x_client is None:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
    return session or x_client

async def get_cookie_or_token(
    session: Optional[str] = Cookie(None),
    token: Optional[str] = Query(None),
):
    if session is None and not token:
        return None

    return session or token

# WebSockets用のエンドポイント
@router.websocket("/ws/send")
async def websocket_endpoint(
    ws: WebSocket
):
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
        #await ws.close()
        # 接続が切れた場合、当該クライアントを削除する
        del clients[key]

# WebSockets用のエンドポイント
@router.websocket("/ws/reception")
async def websocket_endpoint(
    ws: WebSocket
):
    await ws.accept()

    # クライアントを識別するためのIDを取得
    key = ws.headers.get('sec-websocket-key')
    clients[key] = ws
    try:
        while True:
            # 接続中のクライアントそれぞれにメッセージを送信（ブロードキャスト）
            for client in clients.values():
                await client.send_text(f"ID:{key} Message:")
    except websockets.exceptions.ConnectionClosed:
        await ws.close()
        # 接続が切れた場合、当該クライアントを削除する
        del clients[key]