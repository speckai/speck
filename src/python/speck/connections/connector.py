from abc import ABC

from ..chat.entities import ChatLogger, Prompt, Response
from ..logs.logger import universal_format_log
from .providers import Providers


class IConnector(ABC):
    def __init__(self, provider: Providers):
        self.provider = provider

    # @abstractmethod
    # def process_message(self, messages: Messages, model: str) -> str:
    #     pass

    def _get_log_kwargs(self, prompt: Prompt, response: Response, **kwargs):
        return {
            "provider": self.provider,
            "model": kwargs.get("model"),
            "temperature": kwargs.get("temperature"),
            "stream": kwargs.get("stream", False),
            "prompt": prompt,
            "config": kwargs,
            "response": response,
        }

    def log(self, prompt: Prompt, model: str, response: Response, **kwargs):
        ChatLogger.log(**self._get_log_kwargs(prompt, response, **kwargs))

    def __str__(self):
        return f"Client({self.provider.value})"
