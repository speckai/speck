from typing import Literal

from openai import OpenAI

from ..chat.entities import IChatClient, IChatConfig, Messages
from .entities import IConnector, Providers

OpenAIModel = Literal["gpt-4", "gpt-3.5", "gpt-3.5-turbo"]


class OpenAIChatConfig(IChatConfig):
    def __init__(self, temperature: float = 1.0, **kwargs):
        super().__init__(**kwargs)
        self.temperature = temperature


class OpenAIConnector(IConnector, IChatClient):
    def __init__(self, api_key: str):
        super().__init__(provider=Providers.OpenAI)
        self.api_key = api_key
        self.client = OpenAI(api_key=self.api_key)
        print(api_key)

    def _convert_messages_to_prompt(self, messages: Messages) -> list[dict[str, str]]:
        return [{"role": msg.role, "content": msg.content} for msg in messages.messages]

    def chat(
        self,
        messages: Messages,
        model: OpenAIModel,
        temperature: float = 1.0,
        **config_kwargs
    ) -> str:
        print(temperature)
        input = self._convert_messages_to_prompt(messages)
        output = self.client.chat.completions.create(
            messages=input, model=model, temperature=temperature, **config_kwargs
        )
        return output
