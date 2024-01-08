from __future__ import annotations

import logging
from typing import Any, Callable, Iterator

from openai import OpenAI as _OpenAI
from openai import Stream as _Stream

from .. import ChatLogger, ProvidersList, Speck
from ..chat.entities import (ChatConfig, OpenAIChatConfig, Prompt, Response,
                             Stream)
from ..util._wrapper import wrap_method

logger = logging.getLogger(__name__)
logger.info = print


def wrapper(original_method, *args, **kwargs):
    """
    Example of a wrapper function that can be used with add_method_wrapper.

    Args:
        original_method: The original method to be wrapped.
        *args, **kwargs: Arguments and keyword arguments for the original method.

    Returns:
        The result of the original method call.
    """
    logger.info(f"Before calling {original_method.__name__}")
    result = original_method(*args, **kwargs)
    logger.info(f"After calling {original_method.__name__}")
    return result


class OpenAIStream:
    # processor that has lambda which returns MessageDelta
    def __init__(
        self,
        config: OpenAIChatConfig,
        prompt: Prompt,
        iterator: Iterator[Any],
        kwargs: dict,
        processor: Callable[[Any], Any],
        speck_api_key: str,
    ):
        self.config: OpenAIChatConfig = config
        self.prompt = prompt
        self.message: str = ""
        self._iterator = iterator
        self._kwargs = kwargs
        self._processor = processor
        self._has_logged = False
        self._closed = False
        self._last_item = None
        self.speck_api_key = speck_api_key

    def _log(self):
        if not self._has_logged:
            self._has_logged = True

            kwargs = self._kwargs
            kwargs["prompt"] = self._kwargs.get("prompt", [])
            kwargs["model"] = self._kwargs.get("model", "N/A")
            # kwargs["response"] = Response(content=self.message, raw={}, closed=True)
            # ChatLogger.log(**kwargs)

            self.config.log_chat(
                speck_api_key=self.speck_api_key,
                endpoint="https://api.getspeck.ai",
                prompt=self.prompt,
                response=Response(content=self.message, raw={}, closed=True),
            )

    def _process(self, item) -> Any:
        return self._processor(item)

    def __next__(self) -> Any:
        try:
            if self._closed:
                raise StopIteration

            item: Any = self._process(next(self._iterator))
            self._last_item = item
            if item.choices[0].delta.content:
                self.message += item.choices[0].delta.content
            return item
        except StopIteration:
            self._log()
            raise

    def __iter__(self) -> Iterator[Any]:
        return self

    def close(self):
        try:
            self._closed = True
            # todo: make this work for packages other than openai
            self._iterator.response.close()
        except AttributeError:
            pass


def chat_wrapper(self: OpenAIWrapper, original_method, *args, **kwargs):
    """
    Example of a wrapper function that can be used with add_method_wrapper.

    Args:
        original_method: The original method to be wrapped.
        *args, **kwargs: Arguments and keyword arguments for the original method.

    Returns:
        The result of the original method call.
    """
    model: str = kwargs.get("model", None)
    stream = kwargs.get("stream", False)
    messages = kwargs.get("messages", None)
    prompt = Prompt.from_openai(messages)

    config = OpenAIChatConfig(**kwargs)

    if model is not None and ":" in model:
        provider, model = model.split(":", 1)
        if provider in ProvidersList:
            config = config.convert()
            config.provider = provider
            config.model = model
            # Todo: return in OpenAI format
            return self._speck_client.chat.create(prompt=prompt, config=config)

    logger.info(f"Call {original_method.__name__} with model {model}")
    if stream:
        stream = original_method(*args, **kwargs)
        # Todo: wrap the Stream class
        # Best current way to do this is to convert our Stream class to an OpenAI Stream class
        return OpenAIStream(
            config=config,
            prompt=prompt,
            iterator=stream,
            kwargs={
                "provider": "openai",
            },
            processor=lambda a: a,
            speck_api_key=self._speck_api_key,
        )
    else:
        result = original_method(*args, **kwargs)

        config.log_chat(
            speck_api_key=self._speck_api_key,
            endpoint="https://api.getspeck.ai",
            prompt=prompt,
            response=result,
            provider="openai",
        )

        return result


def stream_next_wrapper(original_method, *args, **kwargs):
    print(f"Before calling {original_method.__name__}")
    result = original_method(*args, **kwargs)
    print(f"After calling {original_method.__name__}")
    # print(result)
    return result


def stream_iter_wrapper(original_method, *args, **kwargs):
    print(f"Before calling {original_method.__name__}")
    result = original_method(*args, **kwargs)
    print(f"After calling {original_method.__name__}")
    # print(result)
    return result


class OpenAIWrapper(_OpenAI):
    _speck_api_key: str
    _speck_client: Speck

    def initialize_speck(self, speck_api_key: str, api_keys: dict[str, str] = {}):
        self._speck_api_key = speck_api_key
        if "openai" not in api_keys:
            api_keys["openai"] = self.api_key
        self._speck_client = Speck(api_key=speck_api_key, api_keys=api_keys)


def _wrapper_init(original_method, *args, **kwargs):
    """
    Example of a wrapper function that can be used with add_method_wrapper.

    Args:
        original_method: The original method to be wrapped.
        *args, **kwargs: Arguments and keyword arguments for the original method.

    Returns:
        The result of the original method call.
    """
    logger.info(f"Initializing {original_method.__name__}")
    result = original_method(*args, **kwargs)
    logger.info(f"Adding method wrappers {original_method.__name__}")
    self = args[0]
    wrap_method(
        self.chat.completions,
        "create",
        lambda *args, **kwargs: chat_wrapper(self, *args, **kwargs),
    )
    logger.info(f"After calling {original_method.__name__}")
    return result


wrap_method(OpenAIWrapper, "__init__", _wrapper_init)

# add_method_kwarg(OpenAIWrapper, "__init__", "speck_log", 69)
