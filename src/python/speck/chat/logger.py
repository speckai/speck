from typing import Any

from ..logs.logger import universal_format_log


class ChatLogger:
    @staticmethod
    def log(speck_api_key: str, endpoint: str, prompt: Any, model: str, response: Any, **kwargs):
        if kwargs.get("config", {}).get("_log", True):
            universal_format_log(
                speck_api_key=speck_api_key,
                endpoint=endpoint,
                prompt=prompt,
                model=model,
                response=response,
                **kwargs,
            )
