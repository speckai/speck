from typing import Any

import requests

from ..util import get_dict
from .metadata import generate_metadata_dict


# Todo: Fix typing for this function (circular import)
def universal_format_log(
    speck_api_key: str,
    endpoint: str,
    provider: "Providers",
    prompt: "Prompt",
    model: str,
    response: "Response",
    session_key: str = None,
    **kwargs,
) -> dict[str, str]:
    if not speck_api_key:
        return {}

    body: dict[str, Any] = {
        "input": {
            # Todo: Fix typing for Providers enum (circular import)
            "provider": provider.value if hasattr(provider, "value") else provider,
            "model": model,
            **prompt.to_dict(),
            **kwargs,
        },
        "output": get_dict(response),
        "metadata": generate_metadata_dict(),
    }

    try:
        headers = {"X-API-Key": speck_api_key}
        request: requests.Response = requests.post(
            f"{endpoint}/logging/create/llm", headers=headers, json=body
        )
        request.raise_for_status()
        return request.json()
    except requests.exceptions.HTTPError as e:
        print("HTTP", e)
    except requests.exceptions.ReadTimeout as e:
        print("Read", e)
    except requests.exceptions.ConnectionError as e:
        print("Connection", e)
    except requests.exceptions.RequestException as e:
        print("Request", e)
