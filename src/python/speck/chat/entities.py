from abc import ABC, abstractmethod
from typing import Iterator, Literal

# from dataclasses import dataclass
from pydantic import BaseModel

from ..chat.logger import ChatLogger

MessageRole = Literal["system", "user", "assistant"]


class Message(BaseModel):
    role: MessageRole
    content: str


class Prompt:
    def __init__(self, messages: str | Message | list[Message]):
        # Todo: Handle string, Message, and list[Message]
        self.messages = messages

    @classmethod
    def from_openai(cls, messages: list[dict[str, str]]):
        return cls(
            messages=[
                Message(role=message["role"], content=message["content"])
                for message in messages
            ]
        )
    
    def to_list(self):
        print("To List")
        return [
            {"role": message.role, "content": message.content} for message in self.messages
        ]

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


class MessageDelta(BaseModel):
    content: str


class Stream:
    def __init__(self, iterator, kwargs):
        self._iterator = iterator
        self._kwargs = kwargs
        self._has_logged = False

    def _log(self):
        if not self._has_logged:
            print("Stream logged!")
            self._has_logged = True

            kwargs = self._kwargs
            kwargs["prompt"] = Prompt(messages=[])
            kwargs["model"] = self._kwargs.get("model", "")
            kwargs["response"] = Response(content="", raw={})
            ChatLogger.log(**kwargs)

    def __next__(self) -> Iterator[MessageDelta]:
        try:
            return self._iterator.__next__()
        except StopIteration:
            self._log()
            raise

    def __iter__(self) -> Iterator[MessageDelta]:
        for item in self._iterator:
            yield item

        self._log()


class IChatConfig:
    def __init__(self, **kwargs):
        self.kwargs = kwargs
        # for key, value in kwargs.items():
        #     setattr(self, key, value)


class IChatClient(ABC):
    @abstractmethod
    def chat(
        self,
        prompt: Prompt,
        model: str,
        stream: bool = False,
        config: IChatConfig = IChatConfig(),
        **config_kwargs,
    ) -> Response | Stream:
        pass
