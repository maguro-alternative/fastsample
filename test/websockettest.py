import asyncio
import websockets

async def connect_to_websocket():
    uri = "ws://fastsample-389906.an.r.appspot.com/ws"  # FastAPIサーバーのWebSocketエンドポイントのURIを指定します

    async with websockets.connect(uri) as websocket:
        try:
            # 接続が確立されたらサーバーからのメッセージを待機
            while True:
                message = await websocket.recv()
                print(f"Received message from server: {message}")
        except websockets.exceptions.ConnectionClosed:
            print("Connection to the server is closed.")

if __name__ == "__main__":
    # 非同期イベントループを作成してWebSocketに接続
    asyncio.get_event_loop().run_until_complete(connect_to_websocket())