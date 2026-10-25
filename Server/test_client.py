import asyncio
import json
from websockets.asyncio.client import connect


async def receive_json():
    async with connect("ws://localhost:8765") as websocket:
        async for message in websocket:
            message = json.loads(message)
            print(message)

async def main():
    await receive_json()

if __name__ == "__main__":
    asyncio.run(main())