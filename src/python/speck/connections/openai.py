from ..chat.entities import Messages
from .entities import IConnector


class OpenAIConnector(IConnector):
    def __init__(self, api_key: str):
        self.api_key = api_key

    def _convert_messages_to_prompt(self, messages: Messages) -> str:


    def process_message(self, messages: Messages) -> str:
        # Implement the processing logic specific to OpenAI
        return f"Processed by OpenAI:\n{messages}"
