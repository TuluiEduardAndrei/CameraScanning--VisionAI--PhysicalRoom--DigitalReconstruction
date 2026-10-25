import asyncio
import json
from websockets.asyncio.server import serve

unity = None  # The only connected client

# Called when Unity client connects to the server
async def on_client_connected(connection):
    global unity

    unity = connection
    print("Unity connected!")

    # Keep the connection alive
    await connection.wait_closed()

    print("Unity disconnected!")


async def send_json(data):
    if unity is not None:
        await unity.send(json.dumps(data))


async def main():
    async with serve(on_client_connected, "localhost", 8765) as server:
        print("Server running!")
        # await server.serve_forever()

        while True:
            await asyncio.to_thread(input, "Press ENTER to send JSON: ")

            with open("scene.json", "r") as file:
                data = json.load(file)

            await send_json(data)



if __name__ == "__main__":
    asyncio.run(main())