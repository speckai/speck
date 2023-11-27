from abc import ABC, abstractmethod
from typing import Literal

# from dataclasses import dataclass
from pydantic import BaseModel

from ..connections.entities import IConnector

MessageRole = Literal["system", "user", "assistant"]


class Message(BaseModel):
    role: MessageRole
    content: str


class Messages(BaseModel):
    messages: list[Message]

    def __str__(self):
        return "\n".join(
            [f"{message.role}: {message.content}" for message in self.messages]
        )


class IChatConfig:
    def __init__(self, **kwargs):
        self.kwargs = kwargs
        # for key, value in kwargs.items():
        #     setattr(self, key, value)


class IChatClient(ABC):
    @abstractmethod
    def chat(
        self,
        messages: Messages,
        model: str,
        config: IChatConfig = IChatConfig(),
        **config_kwargs,
    ) -> str:
        pass
