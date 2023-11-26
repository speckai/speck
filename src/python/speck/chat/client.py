from enum import Enum

from pydantic import BaseConfig, BaseModel

from ..chat.entities import Messages
from ..connections.custom import CustomProviderConnector
from ..connections.entities import IConnector, Models
from ..connections.openai import OpenAIConnector


class Providers(Enum):
    OpenAI = "OpenAI"
    CustomProvider = "CustomProvider"


class Client(BaseModel):
    provider: Providers
    provider_config: dict = None
    connector: IConnector = None

    class Config(BaseConfig):
        arbitrary_types_allowed = True

    def __init__(self, provider_config: dict = None, **data):
        super().__init__(**data)
        self.provider_config = provider_config or {}
        self.connector = self._get_connector(**data)

    def _get_connector(self, **data) -> IConnector:
        if self.provider == Providers.OpenAI:
            return OpenAIConnector(
                api_key=self.provider_config.get("api_key", data.get("api_key", ""))
            )
        elif self.provider == Providers.CustomProvider:
            return CustomProviderConnector(
                message_prefix=self.provider_config.get("message_prefix", ""),
                message_suffix=self.provider_config.get("message_suffix", ""),
            )
        raise NotImplementedError("Provider not supported")

    @classmethod
    def from_string(cls, model_str: str):
        provider_str, model_str = model_str.split(":")
        provider = next((p for p in Providers if p.value[0] == provider_str), None)
        if provider is None:
            raise ValueError("Invalid provider")
        return cls(provider=provider)

    def process_message(self, messages: Messages, model: Models) -> str:
        return self.connector.process_message(messages=messages, model=model)

    def __str__(self):
        return f"Client({self.provider.value})"
