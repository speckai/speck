import requests

from ..models.config import ENDPOINT
from .metadata import generate_metadata_dict


class app:
    def log(message: str) -> dict[str, str]:
        body: dict[str, str] = {
            "message": message,
            "metadata": generate_metadata_dict(),
        }
        request: requests.Response = requests.post(
            f"{ENDPOINT}/logging/create/app", json=body
        )
        return request.json()
