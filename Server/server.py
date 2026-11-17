import asyncio
import json
from websockets.asyncio.server import serve

unity = None

# Open Server -> Unity -> Detector in this order
async def on_client_connected(connection):
    global unity

    # First message identifies the client
    message = await connection.recv()
    role = json.loads(message)["role"]

    if role == "unity":
        unity = connection
        print("Unity connected!")

        await connection.wait_closed()

    elif role == "detector":
        print("Detector connected!")

        async for message in connection:
            await unity.send(message)
            print("Scene sent to Unity!")


async def main():
    async with serve(on_client_connected, "0.0.0.0", 8765) as server:
        print("Server running!")
        await server.serve_forever()


if __name__ == "__main__":
    asyncio.run(main())