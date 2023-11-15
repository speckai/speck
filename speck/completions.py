import asyncio
import json

import httpx
import requests

from .chat_format import Message
from .config import ENDPOINT


# Todo: migrate this to its own chat folder
class chat:
    @staticmethod
    def create(
        model: str,
        messages: list[Message] | list[dict[str, str]],
        session_key: str,
        **kwargs,
    ):
        body: dict[str, str] = {
            "model": model,
            "messages": messages,
        }
        request: requests.Response = requests.post(
            f"{ENDPOINT}/completions/create", json=body
        )
        return request.json()
        pass

    @staticmethod
    async def create_async(
        model: str,
        messages: list[Message] | list[dict[str, str]],
        session_key: str,
        **kwargs,
    ):
        # Todo: post async
        pass

    @staticmethod
    async def create_stream(
        model: str,
        messages: list[Message] | list[dict[str, str]],
        session_key: str,
        process_chunk_lambda,
    ):
        body: dict[str, str] = {
            "model": model,
            "messages": messages,
        }

        full_content = []  # List to accumulate the content of each chunk

        async with httpx.AsyncClient() as client:
            async with client.stream(
                "POST", f"{ENDPOINT}/completions/stream", json=body, timeout=None
            ) as response:
                async for chunk in response.aiter_raw():
                    decoded_chunk: str = chunk.decode("utf-8")
                    chunk_data: dict[str, str] = json.loads(decoded_chunk)
                    chunk_type: str = chunk_data.get("type")
                    chunk_content: str = chunk_data.get("content")

                    # Process each chunk with the lambda function
                    process_chunk_lambda(chunk_type, chunk_content)

                    # Accumulate the content
                    full_content.append(chunk_content)

                    # Handle the end of the stream
                    if chunk_type == "full":
                        break

        return "".join(full_content)  # Return the complete message
