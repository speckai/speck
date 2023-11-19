import requests

from speck.metadata import generate_metadata_dict
from speck.models.config import ENDPOINT


def app_log(message: str):
    body: dict[str, str] = {
        "message": message,
        "metadata": generate_metadata_dict(),
    }
    request: requests.Response = requests.post(
        f"{ENDPOINT}/chat/completions/app-log", json=body
    )
    # request.raise_for_status()
    return request.json()
