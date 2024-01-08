import asyncio

import websockets


async def websocket_client():
    uri = "ws://localhost:8080/debug/ws"  # Replace with your server URI
    async with websockets.connect(uri) as websocket:
        await websocket.send("Hello Server!")

        try:
            # Wait for a response with a timeout of 5 seconds
            response = await asyncio.wait_for(websocket.recv(), timeout=5)
            print(f"Received from server: {response}")
        except asyncio.TimeoutError:
            print("No response received from server within 5 seconds")


def run_websocket_client():
    asyncio.run(websocket_client())
    print("hi")


# Call the synchronous function
run_websocket_client()
