from abc import ABC, abstractmethod
from enum import Enum

from ..chat.entities import Messages


class Models(Enum):
    GPT4 = "gpt-4"
    GPT35 = "gpt-3.5"
    GPT35_TURBO = "gpt-3.5-turbo"


class IConnector(ABC):
    @abstractmethod
    def process_message(self, messages: Messages, model: Models) -> str:
        pass
