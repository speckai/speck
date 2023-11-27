from typing import Any

import requests
from openai import ChatCompletion

from ..models.chat_format import Message
from ..models.config import ENDPOINT
from .metadata import generate_metadata_dict


class openai:
    @staticmethod
    def log(
        response: ChatCompletion,
        model: str,
        messages: list[dict[str, str]],
        session_key: str = None,
        **kwargs,
    ) -> dict[str, str]:
        body: dict[str, str] = {
            "input": {
                "model": model,
                "messages": messages,
                **kwargs,
            },
            "output": response.model_dump(),
            "message": response.model_dump()["choices"][0]["message"]["content"],
            "metadata": generate_metadata_dict(),
        }
        request: requests.Response = requests.post(
            f"{ENDPOINT}/logging/create/llm", json=body
        )
        return request.json()

    @staticmethod
    def log_verbose(
        model: str,
        messages: list[Message] | list[dict[str, str]],
        completion: dict[str, str],
        session_key: str = None,
        **kwargs,
    ) -> dict[str, str]:
        body: dict[str, str] = {
            "input": {
                "model": model,
                "messages": messages,
                **kwargs,
            },
            "output": completion,
            "message": completion["choices"][0]["message"]["content"],
            "metadata": generate_metadata_dict(),
        }
        request: requests.Response = requests.post(
            f"{ENDPOINT}/logging/create/llm", json=body
        )
        print(request.json())
        return request.json()
