"""
Name: Anthropic
URL: https://anthropic.ai/
Features:
- Chat
"""
import json
from typing import Union

import requests

from ..chat.entities import (
    NOT_GIVEN,
    ChatConfig,
    IChatClient,
    MessageChunk,
    Prompt,
    Response,
    Stream,
)
from .connector import IConnector
from .providers import Providers


def _process_chunk(obj) -> MessageChunk:
    return MessageChunk(content=obj["completion"])


class AnthropicStream:
    def __init__(self, iterator):
        self.iterator = iterator
        self.closed = False

    def __iter__(self):
        return self

    def __next__(self):
        while True:
            if self.closed:
                raise StopIteration

            obj = next(self.iterator)
            line = obj.decode("utf-8")
            if line.startswith("data: "):
                data = json.loads(line[6:])
                if data.get("stop_reason") is not None:
                    self.closed = True
                if data.get("completion") is not None:
                    return data
            else:
                continue


class AnthropicResponse(Response):
    def __init__(self, obj):
        content = obj["completion"]
        super().__init__(
            content=content,
            prompt_tokens=None,
            completion_tokens=None,
            raw=obj,
        )


class AnthropicConnector(IConnector, IChatClient):
    def __init__(self, client: "Speck" = None, api_key: str = None):
        super().__init__(client=client, provider=Providers.OpenAI)
        if api_key is not None:
            self.api_key = api_key
            self.url = "https://api.anthropic.com/v1/complete"

    def _convert_messages_to_prompt(self, messages: Prompt) -> str:
        res = ""
        if messages.messages[0].role == "system":
            res = "System: " + messages.messages[0].content + "\n\n"
        for msg in messages.messages:
            if msg.role == "system":
                continue
            res += (
                f"{'Human' if msg.role == 'user' else 'Assistant'}: "
                + msg.content
                + "\n\n"
            )
        res += "Assistant:"
        return res

    def chat(
        self, prompt: Prompt, config: ChatConfig = NOT_GIVEN, **config_kwargs
    ) -> Union[AnthropicResponse, Stream]:
        if config is NOT_GIVEN:
            config = ChatConfig(**config_kwargs)
            # Todo: convert to default config based on class param

        # Remove all None values
        all_kwargs = {k: v for k, v in vars(config).items() if v is not None}

        input = self._convert_messages_to_prompt(prompt)

        headers = {
            "anthropic-version": config.get("anthropic_version", "2023-06-01"),
            "content-type": "application/json",
            "x-api-key": self.api_key,
        }

        data = {
            "model": config.model,
            "prompt": input,
            "max_tokens_to_sample": config.max_tokens or 100,
            "stream": config.stream,
        }

        response = requests.post(
            self.url, headers=headers, data=json.dumps(data), stream=config.stream
        )

        if config.stream:
            return Stream(
                client=self._client,
                iterator=AnthropicStream(response.iter_lines()),
                kwargs=self._get_log_kwargs(prompt, None, **all_kwargs),
                processor=_process_chunk,
            )
        else:
            output = response.json()
            if config._log:
                self.log(
                    prompt=prompt,
                    response=AnthropicResponse(output),
                    **all_kwargs,
                )
                # Todo: set config= as param

            return AnthropicResponse(output)
