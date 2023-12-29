import requests

from .metadata import generate_metadata_dict


class app:
    def log(message: str, endpoint: str = "https://api.speck.chat") -> dict[str, str]:
        body: dict[str, str] = {
            "message": message,
            "metadata": generate_metadata_dict(),
        }
        request: requests.Response = requests.post(
            f"{endpoint}/logging/create/app", json=body
        )
        return request.json()
