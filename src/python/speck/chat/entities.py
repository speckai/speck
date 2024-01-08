from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Callable, Iterator, Literal, Optional, Tuple, Union

from openai._types import NotGiven
# from dataclasses import dataclass
from pydantic import BaseModel, Extra

from ..chat.logger import ChatLogger
from ..debug._debug_socket import run_debug_websocket

NOT_GIVEN = None


class Message(BaseModel):
    role: MessageRole
    content: str


class SafeDict(dict):
    def __missing__(self, key):
        return "{" + key + "}"  # Returns the key in curly braces as a string


class Prompt(str):
    messages: list[Message]
    variables: Union[dict[str, str], None] = None

    def to_dict(self):
        return {
            "messages": self.messages,
            "variables": self.variables,
        }

    def __init__(
        self,
        messages: PromptTypes,
        variables: Union[dict[str, str], None] = None,
        **kwargs,
    ):
        if isinstance(messages, str):
            messages = [Message(role="user", content=messages)]
        elif isinstance(messages, Message):
            messages = [messages]
        elif isinstance(messages, list):
            if all(isinstance(message, Message) for message in messages):
                pass
            elif all(isinstance(message, dict) for message in messages):
                messages = [
                    Message(role=message["role"], content=message["content"])
                    for message in messages
                ]
            else:
                raise ValueError(
                    f"Invalid type for messages: {type(messages)}\n{messages}"
                )

        self.messages = messages
        self.variables = variables
        super().__init__()

    @classmethod
    def create(
        cls, messages: PromptTypes, variables: dict[str, str] = None
    ) -> "Prompt":
        if isinstance(messages, cls):
            # Todo: clone object and add variables
            return messages
        return cls(messages=messages, variables=variables)

    @classmethod
    def _read(cls, lines: str) -> "Prompt":
        # Todo: add config parsing
        config = {}
        messages = []

        current_min_spaces = 0
        current_section = None
        current_message = []

        def add_message():
            nonlocal current_message, current_min_spaces
            if current_message:
                messages.append(
                    Message(
                        role=current_section,
                        content="\n".join(
                            [m[current_min_spaces:] for m in current_message]
                        ),
                    )
                )
                current_message = []
                current_min_spaces = 0

        for line in lines.split("\n"):
            line = line.rstrip("\r")
            if line.startswith("<"):
                line = line.strip()
                add_message()
                current_section = line[1:-1].lower()
            elif current_section == "config" and "=" in line:
                key, value = line.split("=", 1)
                config[key.strip()] = value.strip()
            elif current_section in ["system", "user", "assistant"]:
                min_spaces = len(line) - len(line.lstrip())
                if 0 < min_spaces < current_min_spaces or current_min_spaces == 0:
                    current_min_spaces = min_spaces
                current_message.append(line)

        add_message()
        return cls(messages=messages)

    @classmethod
    def read(cls, path: str, name: Union[str, None] = None) -> "Prompt":
        with open(path, "r") as f:
            if name is not None:
                prompts = cls.read_all(path)
                return prompts[name]
            else:
                return cls._read(f.read())

    @classmethod
    def read_all(cls, path: str) -> dict[str, "Prompt"]:
        with open(path, "r") as f:
            prompts = {}
            lines = []
            current_prompt_name = None
            current_min_spaces = -1

            for line in f:
                line = line.rstrip("\n").rstrip("\r")
                if line.lstrip().startswith("<"):
                    min_spaces = len(line) - len(line.lstrip())
                    stripped_line = line.strip()

                    if stripped_line.startswith("<prompt") and min_spaces == 0:
                        if current_prompt_name:
                            prompts[current_prompt_name] = cls._read(
                                "\n".join([m[current_min_spaces:] for m in lines])
                            )
                        current_prompt_name = stripped_line[8:-1].strip()
                        current_min_spaces = -1
                        lines = []
                    elif stripped_line.startswith("</prompt>") and min_spaces == 0:
                        prompts[current_prompt_name] = cls._read(
                            "\n".join([m[current_min_spaces:] for m in lines])
                        )
                        current_prompt_name = None
                        current_min_spaces = -1
                        lines = []
                    else:
                        lines.append(line)
                        if current_min_spaces == -1 or min_spaces < current_min_spaces:
                            current_min_spaces = min_spaces
                else:
                    lines.append(line)

            return prompts

    def _file(self):
        file = []
        for message in self.messages:
            file.append(f"<{message.role.lower()}>")
            for line in message.content.split("\n"):
                file.append(" " * 4 + line)
        return "\n".join(file)

    @classmethod
    def write(cls, prompt: Union["Prompt", dict[str, "Prompt"]], path: str):
        with open(path, "w") as f:
            if isinstance(prompt, dict):
                content = ""
                for name, prompt in prompt.items():
                    content += f"<prompt {name}>\n"
                    content += "\n".join(
                        [" " * 4 + line for line in prompt._file().split("\n")]
                    )
                    content += "\n</prompt>\n\n"
                f.write(content.strip())
            else:
                f.write(prompt._file())

    def __new__(
        cls,
        messages: PromptTypes,
        **kwargs,
    ):
        # Todo: Handle string, Message, and list[Message]
        instance = super(Prompt, cls).__new__(cls, str(messages))
        return instance

    @classmethod
    def from_openai(cls, messages: list[dict[str, str]]):
        return cls(
            messages=[
                Message(role=message["role"], content=message["content"])
                for message in messages
            ]
        )

    def to_list(self):
        return [
            {
                "role": message.role,
                "content": message.content.format_map(SafeDict(self.variables or {})),
            }
            for message in self.messages
        ]

    def to_dict(self):
        return {
            "messages": [
                {"role": message.role, "content": message.content}
                for message in self.messages
            ],
            "variables": self.variables or {},
        }

    @staticmethod
    def _apply_variables(
        messages: list[Message], variables: dict[str, str]
    ) -> list[Message]:
        return [
            Message(
                role=message.role,
                content=message.content.format_map(SafeDict(variables or {})),
            )
            for message in messages
        ]

    def _check_duplicate_keys(self, other_variables: dict[str, str]) -> dict[str, str]:
        duplicate_keys = set((self.variables or {}).keys()).intersection(
            set((other_variables or {}).keys())
        )
        return {
            key: self.variables[key]
            for key in duplicate_keys
            if self.variables[key] != other_variables[key]
        }

    def _remove_duplicate_keys_from_messages(
        self, other_variables: dict[str, str]
    ) -> list[Message]:
        messages = self.messages
        applied_variables = self._check_duplicate_keys(other_variables)
        if len(applied_variables) > 0:
            messages = self._apply_variables(self.messages, applied_variables)

        return messages

    def format(self, *args, **kwargs):
        # return self.__class__(
        #     messages=[
        #         Message(
        #             role=message.role, content=message.content.format(*args, **kwargs)
        #         )
        #         for message in self.messages
        #     ]
        # )

        messages = self._remove_duplicate_keys_from_messages(kwargs)
        return self.__class__(
            messages=[
                Message(role=message.role, content=message.content)
                for message in messages
            ],
            variables={**SafeDict(self.variables or {}), **kwargs},
        )

    def __add__(self, other):
        if isinstance(other, Message):
            return self.__class__(
                messages=self.messages + [other], variables={**(self.variables or {})}
            )
        elif isinstance(other, Prompt):
            # Check if there are duplicate keys
            messages = self._remove_duplicate_keys_from_messages(other.variables or {})

            return self.__class__(
                messages=messages + other.messages,
                variables={
                    **SafeDict(self.variables or {}),
                    **SafeDict(other.variables or {}),
                },
            )
        else:
            raise NotImplementedError

    def __str__(self):
        return (
            "\n".join(
                [f"{message.role}: {message.content}" for message in self.messages]
            )
            + "\n"
            + str(self.variables or {})
        )


class Response(BaseModel):
    content: str
    prompt_tokens: Union[int, None] = None
    completion_tokens: Union[int, None] = None
    raw: Union[dict, None] = None

    def __init__(
        self,
        content: str,
        closed: bool = False,
        prompt_tokens: Union[int, None] = None,
        completion_tokens: Union[int, None] = None,
        raw: Union[dict, None] = None,
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

    @classmethod
    def create(cls, response: ResponseTypes) -> "Response":
        if isinstance(response, cls):
            return response
        elif isinstance(response, str):
            return cls(content=response)
        else:
            raise NotImplementedError

    def __str__(self):
        return f"Response({self.content}, raw={self.raw})"


class MessageChunk(BaseModel):
    content: Union[str, None]

    def encode(self, encoding: str = "utf-8"):
        content = self.content or ""
        return content.encode(encoding)


class Stream:
    # processor that has lambda which returns MessageDelta
    def __init__(
        self,
        client: "Speck",
        iterator: Iterator[Any],
        kwargs: dict,
        log_config: "LogConfig",
        processor: Callable[[Any], MessageChunk],
    ):
        self._client = client
        self.message: str = ""
        self.tokens: int = 0
        self._iterator = iterator
        self._kwargs = kwargs
        self._processor = processor
        self._has_logged = False
        self._closed = False
        self._log_config = log_config

    def _log(self):
        if not self._has_logged:
            self._has_logged = True

            kwargs = self._kwargs
            kwargs["prompt"] = self._kwargs.get("prompt", [])
            kwargs["temperature"] = self._kwargs.get("temperature", "N/A")
            kwargs["model"] = self._kwargs.get("model", "N/A")
            kwargs["response"] = Response(
                content=self.message, raw={}, closed=True, completion_tokens=self.tokens
            )

            # Todo: add prompt_tokens using tiktoken
            ChatLogger.log(log_config=self._log_config, **kwargs)

    def _process(self, item) -> MessageChunk:
        return self._processor(item)

    def __next__(self) -> MessageChunk:
        try:
            if self._closed:
                raise StopIteration

            # next_item = None
            # while next_item is None:
            next_item = next(self._iterator)

            item: MessageChunk = self._process(next_item)
            if item.content:
                self.message += item.content
            self.tokens += 1
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


class LogConfig(BaseModel):
    api_key: str
    endpoint: str = "https://api.getspeck.ai"

    class Config:
        extra = "allow"


class ChatConfig:
    # Todo: add typed params here
    # Todo: Create conversions to other formats
    def __init__(
        self,
        *,
        provider: str = None,
        model: OpenAIModel,
        stream: bool = False,
        _log: bool = True,
        temperature: Union[Optional[float], NotGiven] = NOT_GIVEN,
        max_tokens: Union[Optional[int], NotGiven] = NOT_GIVEN,
        top_p: Union[Optional[float], NotGiven] = NOT_GIVEN,
        frequency_penalty: Union[Optional[float], NotGiven] = NOT_GIVEN,
        presence_penalty: Union[Optional[float], NotGiven] = NOT_GIVEN,
        **config_kwargs,
    ):
        if "log_config" in config_kwargs:
            del config_kwargs["log_config"]

        self.provider = provider
        self.model = model
        self.stream = stream
        self._log = _log
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.top_p = top_p
        self.frequency_penalty = frequency_penalty
        self.presence_penalty = presence_penalty
        self.chat_args = config_kwargs
        # If this is modified, update to_dict too

    def to_dict(self):
        return {
            "provider": self.provider,
            "model": str(self.model),  # Assuming model can be represented as a string
            "stream": self.stream,
            "_log": self._log,
            "temperature": self._convert_optional(self.temperature),
            "max_tokens": self._convert_optional(self.max_tokens),
            "top_p": self._convert_optional(self.top_p),
            "frequency_penalty": self._convert_optional(self.frequency_penalty),
            "presence_penalty": self._convert_optional(self.presence_penalty),
            "chat_args": self.chat_args,
        }

    def _convert_optional(self, value):
        return None if isinstance(value, NotGiven) else value

    @classmethod
    def create(cls, config: ChatConfigTypes, kwargs: dict = None) -> "ChatConfig":
        if isinstance(config, cls):
            if kwargs is not None:
                return cls(**{**config.__dict__, **kwargs})
            else:
                return config
        elif isinstance(config, dict):
            return cls(**config)
        elif kwargs:
            return cls(**kwargs)
        else:
            raise NotImplementedError

    def get(self, key: str, default: Any = None) -> Any:
        return getattr(self, key, default)

    def convert(self, provider: str = "speck") -> "ChatConfig":
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

    def log_chat(
        self,
        *,
        log_config: LogConfig,
        prompt: Prompt,
        response: Response,
        provider: str = "speck",
    ):
        config = self.convert()
        ChatLogger.log(
            log_config=log_config,
            provider=provider,
            model=str(config.model),
            prompt=prompt,
            response=response,
            **config.chat_args,
        )

    def encode(self, encoding: str = "utf-8"):
        return self.__str__().encode(encoding)

    def __str__(self):
        return f"ChatConfig(provider={self.provider}, model={self.model}, stream={self.stream}, _log={self._log}, temperature={self.temperature}, max_tokens={self.max_tokens}, top_p={self.top_p}, frequency_penalty={self.frequency_penalty}, presence_penalty={self.presence_penalty}, _kwargs={self._kwargs})"


class OpenAIChatConfig(ChatConfig):
    def __init__(
        self,
        model: OpenAIModel,
        stream: bool = False,
        _log: bool = True,
        temperature: Union[Optional[float], NotGiven] = NOT_GIVEN,
        max_tokens: Union[Optional[int], NotGiven] = NOT_GIVEN,
        top_p: Union[Optional[float], NotGiven] = NOT_GIVEN,
        frequency_penalty: Union[Optional[float], NotGiven] = NOT_GIVEN,
        presence_penalty: Union[Optional[float], NotGiven] = NOT_GIVEN,
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
    def debug_chat(
        self, prompt: "Prompt", config: "ChatConfig"
    ) -> ("Prompt", "ChatConfig"):
        data = run_debug_websocket(self._client, self, prompt, config)

        print(data)
        if data.get("prompt") and data.get("config"):
            prompt = Prompt(**data["prompt"])
            config = ChatConfig(**data["config"])

        return prompt, config

    @abstractmethod
    def chat(
        self,
        prompt: PromptTypes,
        config: Union[ChatConfig, NotGiven] = NOT_GIVEN,
        **config_kwargs,
    ) -> Union[Response, Stream]:
        pass

    @abstractmethod
    async def achat(
        self,
        prompt: PromptTypes,
        config: Union[ChatConfig, NotGiven] = NOT_GIVEN,
        **config_kwargs,
    ) -> Union[Response, Stream]:
        pass


PromptTypes = Union[str, Message, list[Message], list[dict[str, str]]]
ResponseTypes = Union[Response, str]
ChatConfigTypes = Union[ChatConfig, dict[str, str]]

MessageRole = Literal["system", "user", "assistant"]
OpenAIModel = Tuple[Literal["gpt-4", "gpt-3.5", "gpt-3.5-turbo"], str]
