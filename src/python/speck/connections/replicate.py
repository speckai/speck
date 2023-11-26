from ..chat.entities import Messages
from .entities import IConnector


class CustomProviderConnector(IConnector):
    def __init__(self, message_prefix: str, message_suffix: str):
        self.message_prefix = message_prefix
        self.message_suffix = message_suffix

    def process_message(self, messages: Messages) -> str:
        return f"{self.message_prefix} {messages} {self.message_suffix}"