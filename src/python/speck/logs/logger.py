from typing import Any

import requests

from ..chat.entities import Prompt, Response
from ..connections.providers import Providers
from ..models import ENDPOINT
from .app import app
from .metadata import generate_metadata_dict
from .openai import openai


def universal_format_log(
    provider: Providers | str,
    prompt: Prompt,
    model: str,
    response: Response,
    session_key: str = None,
    **kwargs,
) -> dict[str, str]:
    body: dict[str, Any] = {
        "input": {
            "provider": provider.value if type(provider) == Providers else provider,
            "model": model,
            "messages": prompt.model_dump()["messages"],
            **kwargs,
        },
        "output": response.model_dump(),
        "metadata": generate_metadata_dict(),
    }

    try:
        request: requests.Response = requests.post(
            f"{ENDPOINT}/logging/create/llm", json=body
        )
        return request.json()
    except requests.exceptions.HTTPError as e:
        print("HTTP", e)
    except requests.exceptions.ReadTimeout as e:
        print("Read", e)
    except requests.exceptions.ConnectionError as e:
        print("Connection", e)
    except requests.exceptions.RequestException as e:
        print("Request", e)
