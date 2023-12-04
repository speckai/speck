from abc import ABC, abstractmethod
from typing import Any, Callable, Iterator, Literal

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
    def from_list(cls, messages: list[dict[str, str]]):
        return cls(
            messages=[
                Message(role=message["role"], content=message["content"])
                for message in messages
            ]
        )

    def to_list(self):
        print("To List")
        return [
            {"role": message.role, "content": message.content}
            for message in self.messages
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
    content: str | None


class Stream:
    # processor that has lambda which returns MessageDelta
    def __init__(
        self,
        iterator: Iterator[Any],
        kwargs: dict,
        processor: Callable[[Any], MessageDelta],
    ):
        self._iterator = iterator
        self._kwargs = kwargs
        self._processor = processor
        self._has_logged = False
        self._closed = False

    def _log(self):
        if not self._has_logged:
            print("Stream logged!")
            self._has_logged = True

            kwargs = self._kwargs
            kwargs["prompt"] = self._kwargs.get("prompt", [])
            kwargs["model"] = self._kwargs.get("model", "N/A")
            kwargs["response"] = Response(content=self.message, raw={})
            ChatLogger.log(**kwargs)

    def _process(self, item) -> MessageDelta:
        return self._processor(item)

    def __next__(self) -> MessageDelta:
        if self._closed:
            raise StopIteration

        try:
            return self._process(self._iterator.__next__())
        except StopIteration:
            self._log()
            raise

    def __iter__(self) -> Iterator[MessageDelta]:
        if self._closed:
            return

        self.message: str = (
            ""  # TODO: Do this in a more raw fashion without needing to iterate
        )
        for item in self._iterator:
            item: MessageDelta = self._process(item)
            # content: str = item if isinstance(item, str) else getattr(item.choices[0].delta, 'content', None)
            if item.content:
                self.message += item.content
            yield item
        self._log()

    def close(self):
        try:
            self._closed = True
            # todo: make this work for packages other than openai
            self._iterator.response.close()
        except AttributeError:
            pass


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
