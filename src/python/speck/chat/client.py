from enum import Enum

from pydantic import BaseConfig, BaseModel

from ..chat.entities import Messages
from ..connections.custom import CustomProviderConnector
from ..connections.entities import IConnector
from ..connections.openai import OpenAIConnector


class Providers(Enum):
    OpenAI = "OpenAI"
    CustomProvider = "CustomProvider"


class Models(Enum):
    GPT4 = "gpt-4"
    GPT35 = "gpt-3.5"
    GPT35_TURBO = "gpt-3.5-turbo"


class Client(BaseModel):
    provider: Providers
    model: Models
    connector: IConnector = None
    provider_config: dict = None

    class Config(BaseConfig):
        arbitrary_types_allowed = True

    def __init__(self, provider_config: dict = None, **data):
        super().__init__(**data)
        self.provider_config = provider_config or {}
        self.connector = self._get_connector()

    def _get_connector(self) -> IConnector:
        if self.provider == Providers.OpenAI:
            return OpenAIConnector(api_key=self.provider_config.get("api_key", ""))
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
        return cls(provider=provider, model=Models(model_str))

    def process_message(self, message: Messages) -> str:
        return self.connector.process_message(message)

    def __str__(self):
        return f"Client({self.provider.value}:{self.model.value})"
