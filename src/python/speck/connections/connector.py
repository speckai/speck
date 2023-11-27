from abc import ABC

from ..chat.entities import Prompt, Response
from ..logs.logger import universal_format_log
from .providers import Providers


class IConnector(ABC):
    def __init__(self, provider: Providers):
        self.provider = provider

    # @abstractmethod
    # def process_message(self, messages: Messages, model: str) -> str:
    #     pass

    def log(self, prompt: Prompt, model: str, response: Response, **kwargs):
        universal_format_log(
            provider=self.provider,
            prompt=prompt,
            model=model,
            response=response,
            **kwargs,
        )

    def __str__(self):
        return f"Client({self.provider.value})"
