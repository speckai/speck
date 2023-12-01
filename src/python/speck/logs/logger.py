from typing import Any

import requests

from ..models import ENDPOINT
from .app import app
from .metadata import generate_metadata_dict
from .openai import openai


# Todo: Fix typing for this function (circular import)
def universal_format_log(
    provider: "Providers",
    prompt: "Prompt",
    model: str,
    response: "Response",
    session_key: str = None,
    **kwargs,
) -> dict[str, str]:
    body: dict[str, Any] = {
        "input": {
            # Todo: Fix typing for Providers enum (circular import)
            "provider": provider.value if hasattr(provider, "value") else provider,
            "model": model,
            "messages": prompt.to_list(),
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
