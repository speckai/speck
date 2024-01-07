from typing import Any

from ..logs.logger import universal_format_log


class ChatLogger:
    @staticmethod
    def log(log_config: "LogConfig", prompt: Any, model: str, response: Any, **kwargs):
        if kwargs.get("config", {}).get("_log", True):
            universal_format_log(
                log_config=log_config,
                prompt=prompt,
                model=model,
                response=response,
                **kwargs,
            )
