from abc import ABC, abstractmethod
from typing import Any, Callable, Iterator, Literal, Optional, Self

from openai._types import NotGiven

# from dataclasses import dataclass
from pydantic import BaseModel

from ..chat.logger import ChatLogger

MessageRole = Literal["system", "user", "assistant"]
OpenAIModel = Literal["gpt-4", "gpt-3.5", "gpt-3.5-turbo"]
NOT_GIVEN = None


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
        closed: bool = False,
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


class MessageChunk(BaseModel):
    content: str | None


class Stream:
    # processor that has lambda which returns MessageDelta
    def __init__(
        self,
        iterator: Iterator[Any],
        kwargs: dict,
        processor: Callable[[Any], MessageChunk],
    ):
        self.message: str = ""
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
            kwargs["response"] = Response(content=self.message, raw={}, closed=True)
            ChatLogger.log(**kwargs)

    def _process(self, item) -> MessageChunk:
        return self._processor(item)

    def __next__(self) -> MessageChunk:
        try:
            if self._closed:
                raise StopIteration

            item: MessageChunk = self._process(next(self._iterator))
            if item.content:
                self.message += item.content
            return item
        except StopIteration:
            self._log()
            raise

    def __iter__(self) -> Iterator[MessageChunk]:
        return self

    def close(self):
        try:
            self._closed = True
            # todo: make this work for packages other than openai
            self._iterator.response.close()
        except AttributeError:
            pass


class ChatConfig:
    # Todo: add typed params here

    # Todo: Create universal config format
    # Todo: Create conversions to other formats
    def __init__(
        self,
        model: OpenAIModel,
        stream: bool = False,
        _log: bool = True,
        temperature: Optional[float] | NotGiven = NOT_GIVEN,
        max_tokens: Optional[int] | NotGiven = NOT_GIVEN,
        top_p: Optional[float] | NotGiven = NOT_GIVEN,
        frequency_penalty: Optional[float] | NotGiven = NOT_GIVEN,
        presence_penalty: Optional[float] | NotGiven = NOT_GIVEN,
        **config_kwargs,
    ):
        self.model = model
        self.stream = stream
        self._log = _log
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.top_p = top_p
        self.frequency_penalty = frequency_penalty
        self.presence_penalty = presence_penalty
        self._kwargs = config_kwargs

    def convert(self, provider: str = "speck") -> Self:
        """
        Convert to another config format
        """
        if provider == "openai":
            return OpenAIChatConfig(
                model=self.model,
                stream=self.stream,
                _log=self._log,
                temperature=self.temperature,
                max_tokens=self.max_tokens,
                top_p=self.top_p,
                frequency_penalty=self.frequency_penalty,
                presence_penalty=self.presence_penalty,
                **self._kwargs,
            )

        return self

    def log_chat(self, prompt: Prompt, response: Response, provider: str = "speck"):
        config = self.convert()
        ChatLogger.log(
            provider=provider,
            model=config.model,
            prompt=prompt,
            response=response,
            **config._kwargs,
        )


class OpenAIChatConfig(ChatConfig):
    def __init__(
        self,
        model: OpenAIModel,
        stream: bool = False,
        _log: bool = True,
        temperature: Optional[float] | NotGiven = NOT_GIVEN,
        max_tokens: Optional[int] | NotGiven = NOT_GIVEN,
        top_p: Optional[float] | NotGiven = NOT_GIVEN,
        frequency_penalty: Optional[float] | NotGiven = NOT_GIVEN,
        presence_penalty: Optional[float] | NotGiven = NOT_GIVEN,
        **config_kwargs,
    ):
        self.model = model
        self.stream = stream
        self._log = _log
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.top_p = top_p
        self.frequency_penalty = frequency_penalty
        self.presence_penalty = presence_penalty
        self._kwargs = config_kwargs

    def convert(self, provider: str = "speck") -> ChatConfig:
        """
        Maps config to universal format then converts to another config format
        """
        universal_config = ChatConfig(
            model=self.model,
            stream=self.stream,
            _log=self._log,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            top_p=self.top_p,
            frequency_penalty=self.frequency_penalty,
            presence_penalty=self.presence_penalty,
            **self._kwargs,
        )

        return universal_config.convert(provider=provider)


class IChatClient(ABC):
    @abstractmethod
    def chat(
        self,
        prompt: Prompt,
        config: ChatConfig | NotGiven = NOT_GIVEN,
        **config_kwargs,
    ) -> Response | Stream:
        pass
