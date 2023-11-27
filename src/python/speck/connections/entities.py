from abc import ABC
from enum import Enum

from pydantic import BaseModel


class Providers(Enum):
    OpenAI = "OpenAI"
    CustomProvider = "CustomProvider"
    Replicate = "Replicate"


class IConnector(ABC):
    def __init__(self, provider: Providers):
        self.provider = provider

    # @abstractmethod
    # def process_message(self, messages: Messages, model: str) -> str:
    #     pass

    def __str__(self):
        return f"Client({self.provider.value})"
