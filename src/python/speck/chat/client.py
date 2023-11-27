from enum import Enum
from typing import Union

from pydantic import BaseConfig, BaseModel

from ..chat.entities import IChatClient, IChatConfig, Messages
from ..connections.custom import CustomProviderConnector
from ..connections.openai import OpenAIConnector
from ..connections.replicate import ReplicateConnector


class Providers(Enum):
    OpenAI = "OpenAI"
    CustomProvider = "CustomProvider"
    Replicate = "Replicate"


class Client(BaseModel, IChatClient):
    provider: Providers
    provider_config: dict = None
    connector: IChatClient = None

    class Config(BaseConfig):
        arbitrary_types_allowed = True

    def __init__(self, provider_config: dict = None, **data):
        super().__init__(**data)
        self.provider_config = provider_config or {}
        self.connector = self._get_connector(**data)

    def _get_connector(self, **data) -> IChatClient:
        if self.provider == Providers.OpenAI:
            return OpenAIConnector(
                api_key=self.provider_config.get("api_key", data.get("api_key", ""))
            )
        elif self.provider == Providers.CustomProvider:
            return CustomProviderConnector(
                message_prefix=self.provider_config.get("message_prefix", ""),
                message_suffix=self.provider_config.get("message_suffix", ""),
            )
        elif self.provider == Providers.Replicate:
            return ReplicateConnector()
        raise NotImplementedError("Provider not supported")

    @classmethod
    def from_string(cls, model_str: str):
        provider_str, model_str = model_str.split(":")
        provider = next((p for p in Providers if p.value[0] == provider_str), None)
        if provider is None:
            raise ValueError("Invalid provider")
        return cls(provider=provider)

    @classmethod
    def from_openai(cls, api_key: str) -> OpenAIConnector:
        return cls(provider=Providers.OpenAI, provider_config={"api_key": api_key})

    @classmethod
    def from_replicate(cls, api_key: str | None = None) -> ReplicateConnector:
        """Reads api_key from environment variable if not provided"""
        return cls(
            provider=Providers.Replicate,
        )

    def chat(self, messages: Messages, model: str, **config_kwargs) -> str:
        return self.connector.chat(messages=messages, model=model, **config_kwargs)

    def __str__(self):
        return f"Client({self.provider.value})"
