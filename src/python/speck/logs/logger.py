import warnings
from typing import Any

import requests

from ..util import get_dict
from .metadata import generate_metadata_dict


# Todo: Fix typing for this function (circular import)
def universal_format_log(
    log_config: "LogConfig",
    provider: "Providers",
    prompt: "Prompt",
    model: str,
    response: "Response",
    session_key: str = None,
    **kwargs,
) -> dict[str, str]:
    if not log_config:
        raise ValueError("No log config found. Define the log config in the log or client.")
    if not log_config.api_key:
        raise ValueError("No valid API key found. Define the API key for the log config.")
    if not log_config.endpoint:
        raise ValueError("No valid endpoint found. Define the endpoint for the log config.")
    
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
        headers = {"X-API-Key": log_config.api_key}
        request: requests.Response = requests.post(
            f"{log_config.endpoint}/logging/create/llm", headers=headers, json=body
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
