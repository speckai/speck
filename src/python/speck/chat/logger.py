from typing import Any

from ..logs.logger import universal_format_log


class ChatLogger:
    @staticmethod
    def log(prompt: Any, model: str, response: Any, **kwargs):
        if kwargs.get("config", {}).get("_log", False):
            universal_format_log(
                prompt=prompt,
                model=model,
                response=response,
                **kwargs,
            )
