import requests

from .metadata import generate_metadata_dict


class app:
    api_key: str = None

    @classmethod
    def set_api_key(cls, api_key: str) -> None:
        cls.api_key = api_key

    @classmethod
    def log(
        cls, message: str, endpoint: str = "https://api.getspeck.ai"
    ) -> dict[str, str]:
        if not cls.api_key:
            return {}

        body: dict[str, str] = {
            "message": message,
            "metadata": generate_metadata_dict(),
        }

        headers = {"X-API-Key": cls.api_key}
        request: requests.Response = requests.post(
            f"{endpoint}/logging/create/app", headers=headers, json=body
        )
        return request.json()
