import asyncio
import websockets, ssl

async def hello():
    uri = "ws://fastsample-389906.an.r.appspot.com/ws"
    async with websockets.connect(
        uri=uri
    ) as websocket:
        await websocket.send("Hello world!")
        print(await websocket.recv())

if __name__ == "__main__":
    asyncio.run(hello())
