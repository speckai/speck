from ..chat.entities import IChatClient, Prompt, Response
from .connector import IConnector
from .providers import Providers


class CustomProviderConnector(IConnector, IChatClient):
    def __init__(self, message_prefix: str, message_suffix: str):
        super().__init__(provider=Providers.CustomProvider)
        self.message_prefix = message_prefix
        self.message_suffix = message_suffix

    def chat(self, prompt: Prompt, model: str, **config_kwargs) -> Response:
        return Response(f"{self.message_prefix} {prompt} {self.message_suffix}")
