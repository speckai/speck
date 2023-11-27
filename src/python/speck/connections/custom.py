from ..chat.entities import IChatClient, IChatConfig, Messages
from .entities import IConnector


class CustomProviderConnector(IConnector, IChatClient):
    def __init__(self, message_prefix: str, message_suffix: str):
        self.message_prefix = message_prefix
        self.message_suffix = message_suffix

    def chat(self, messages: Messages, model: str, **config_kwargs) -> str:
        return f"{self.message_prefix} {messages} {self.message_suffix}"
