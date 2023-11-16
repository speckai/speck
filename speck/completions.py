import asyncio
import json
import os

import httpx
import requests
from openai import OpenAI

from .chat_format import Message
from .config import ENDPOINT
from .metadata import generate_metadata_dict

client = OpenAI(api_key="hi")


def get_api_key():
    return os.environ["OPENAI_API_KEY"]


# Todo: migrate this to its own chat folder
class chat:
    @staticmethod
    def log(
        model: str,
        messages: list[Message] | list[dict[str, str]],
        completion: dict[str, str],
        session_key: str = None,
        **kwargs,
    ):
        body: dict[str, str] = {
            "model": model,
            "messages": messages,
            "completion": completion,
            **kwargs,
            **generate_metadata_dict(),
        }
        request: requests.Response = requests.post(
            f"{ENDPOINT}/chat/completions/log", json=body
        )
        # request.raise_for_status()
        return request.json()

    @staticmethod
    def create(
        model: str,
        messages: list[Message] | list[dict[str, str]],
        session_key: str = None,
        local_retry: bool = True,
        **kwargs,
    ):
        try:
            body: dict[str, str] = {
                "model": model,
                "messages": messages,
            }
            request: requests.Response = requests.post(
                f"{ENDPOINT}/chat/completions/create", json=body
            )
            request.raise_for_status()
            return request.json()
        except requests.exceptions.HTTPError as e:
            if local_retry and get_api_key() is not None:
                print("Failed to create completions, retrying with local API key")
                return client.chat.completions.create(
                    messages=messages,
                    model=model,
                )
            else:
                raise e
        except requests.exceptions.ReadTimeout as errrt:
            print("Time out")
        except requests.exceptions.ConnectionError as conerr:
            print("Connection error")
        except requests.exceptions.RequestException as errex:
            print("Exception request")

    @staticmethod
    async def create_async(
        model: str,
        messages: list[Message] | list[dict[str, str]],
        session_key: str,
        **kwargs,
    ):
        # Todo: post async
        pass

    # Convert streaming to the following format:
    # for text, chunk in chat.stream(model, messages, session_key):
    @staticmethod
    def create_stream(
        model: str,
        messages: list[Message] | list[dict[str, str]],
        process_chunk_lambda,
        session_key: str = None,
    ):
        body: dict[str, str] = {
            "model": model,
            "messages": messages,
        }

        with httpx.Client() as client:
            with client.stream(
                "POST", f"{ENDPOINT}/chat/completions/stream", json=body, timeout=None
            ) as response:
                for chunk in response.iter_raw():
                    decoded_chunk: str = chunk.decode("utf-8")
                    chunk_data: dict[str, str] = json.loads(decoded_chunk)
                    chunk_type: str = chunk_data.get("type")
                    chunk_content: str = chunk_data.get("content")

                    # Process each chunk with the lambda function
                    process_chunk_lambda(chunk_content, chunk_type == "full")

                    # Handle the end of the stream
                    if chunk_type == "full":
                        return chunk_content
