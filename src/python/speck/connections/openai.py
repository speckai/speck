from enum import Enum

from openai import OpenAI

from ..chat.entities import Messages
from .entities import IConnector, Models


class OpenAIConnector(IConnector):
    def __init__(self, api_key: str):
        print(api_key)
        self.api_key = api_key
        self.client = OpenAI(api_key=self.api_key)

    def _convert_messages_to_prompt(self, messages: Messages) -> list[dict[str, str]]:
        return [{"role": msg.role, "content": msg.content} for msg in messages.messages]

    def _get_model(self, model: Models) -> str:
        if model == Models.GPT35_TURBO:
            return "gpt-3.5-turbo"

    def process_message(self, messages: Messages, model: Models = None) -> str:
        input = self._convert_messages_to_prompt(messages)
        output = self.client.chat.completions.create(
            messages=input, model=self._get_model(model)
        )
        return output
