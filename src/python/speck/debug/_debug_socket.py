import asyncio
import json

import websockets


async def _websocket_client(client, connector, prompt, config):
    uri = "ws://localhost:8080/debug/ws"  # Replace with your server URI
    async with websockets.connect(uri) as websocket:
        data = json.dumps(
            {
                "prompt": prompt.to_dict(),
                "config": config.to_dict(),
                "speck": client.to_dict(),
            }
        )
        # "connector": client.connector.to_dict()
        print(data)
        await websocket.send(data)

        try:
            # Wait for a response with a timeout of 5 seconds
            response = await asyncio.wait_for(websocket.recv(), timeout=600)
            print(f"Received from server: {json.loads(response)}")
            return json.loads(response)
        except asyncio.TimeoutError:
            print("No response received from server within 5 seconds")


def run_debug_websocket(client, connector, prompt, config):
    data = asyncio.run(_websocket_client(client, connector, prompt, config))
    return data


if __name__ == "__main__":
    # Call the synchronous function
    run_debug_websocket(None, None)
