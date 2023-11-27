from abc import ABC, abstractmethod
from typing import Literal

# from dataclasses import dataclass
from pydantic import BaseModel

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


class Response(BaseModel):
    content: str
    prompt_tokens: int | None = None
    completion_tokens: int | None = None
    raw: dict | None = None

    def __init__(
        self,
        content: str,
        prompt_tokens: int | None = None,
        completion_tokens: int | None = None,
        raw: dict | None = None,
        **kwargs,
    ):
        super().__init__(
            content=content,
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            raw=raw,
        )
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __str__(self):
        return f"Response({self.content}, raw={self.raw})"


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
    ) -> Response:
        pass
