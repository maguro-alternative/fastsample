import asyncio
import websockets

from http.client import IncompleteRead

URI = "ws://fastsample-389906.an.r.appspot.com/ws"  # FastAPIサーバーのWebSocketエンドポイントのURIを指定します
#URI = "ws://localhost:8080/ws"

async def connect_to_websocket():
    print("is this working?")
    async with websockets.connect(uri=URI) as websocket:
        print("is connection...")
        try:
            print("is connection...")
            # 接続が確立されたらサーバーからのメッセージを待機
            while True:
                message = await websocket.recv()
                print(f"Received message from server: {message}")
        except websockets.exceptions.ConnectionClosed:
            print("Connection to the server is closed.")

async def websocket_client():
    async with websockets.connect(
        uri=URI,
        ping_interval=None,
        ping_timeout=30,
        max_queue=10000
    ) as websocket:
        try:
            while True:
                message = input("Enter a message to send to the server: ")
                await websocket.send(message)  # サーバーにメッセージを送信

                response = await websocket.recv()  # サーバーからのメッセージを受信
                print(f"Received from server: {response}")

        except KeyboardInterrupt:
            print("Connection closed.")
            await websocket.close()

async def hello():
    async with websockets.connect(URI) as websocket:
        await websocket.send("Hello world! 1")
        await websocket.send("Hello world! 2")
        await asyncio.sleep(5.0)
        print(await websocket.recv())
        print(await websocket.recv())


if __name__ == "__main__":
    # 非同期イベントループを作成してWebSocketに接続
    #asyncio.get_event_loop().run_until_complete(connect_to_websocket())
    asyncio.get_event_loop().run_until_complete(websocket_client())
    #asyncio.run(hello())