from ..chat.entities import IChatClient, IChatConfig, Messages, Response
from .entities import IConnector, Providers


class CustomProviderConnector(IChatClient):
    def __init__(self, message_prefix: str, message_suffix: str):
        super().__init__(provider=Providers.CustomProvider)
        self.message_prefix = message_prefix
        self.message_suffix = message_suffix

    def chat(self, messages: Messages, model: str, **config_kwargs) -> Response:
        return Response(f"{self.message_prefix} {messages} {self.message_suffix}")
