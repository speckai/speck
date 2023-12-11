"""
Name: OpenAI
URL: https://platform.openai.com/docs/api-reference
Features:
- Chat
- Vision
- Text-to-Speech
- Speech-to-Text
"""
from typing import Literal, Optional

from openai import OpenAI
from openai._types import NotGiven
from openai.types.chat import ChatCompletion

from ..chat.entities import (
    NOT_GIVEN,
    ChatConfig,
    IChatClient,
    MessageChunk,
    OpenAIChatConfig,
    Prompt,
    Response,
    Stream,
)
from ..util import filter_kwargs
from .connector import IConnector
from .providers import Providers


def _process_chunk(obj) -> MessageChunk:
    return MessageChunk(content=obj.choices[0].delta.content)


class OpenAIResponse(Response):
    def __init__(self, chat_completion: ChatCompletion):
        print(chat_completion)
        content = chat_completion.choices[0].message.content
        super().__init__(
            content=content,
            prompt_tokens=chat_completion.usage.prompt_tokens,
            completion_tokens=chat_completion.usage.completion_tokens,
            raw=chat_completion.model_dump(),
        )


class OpenAIConnector(IConnector, IChatClient):
    def __init__(self, api_key: str):
        super().__init__(provider=Providers.OpenAI)
        self.api_key = api_key
        self.client = OpenAI(api_key=self.api_key)
        print(api_key)

    def _convert_messages_to_prompt(self, messages: Prompt) -> list[dict[str, str]]:
        return [{"role": msg.role, "content": msg.content} for msg in messages.messages]

    def chat(
        self, prompt: Prompt, config: ChatConfig = NOT_GIVEN, **config_kwargs
    ) -> OpenAIResponse | Stream:
        if config is NOT_GIVEN:
            config = ChatConfig(**config_kwargs)
            # Todo: convert to default config based on class param

        # Remove all None values
        all_kwargs = {k: v for k, v in vars(config).items() if v is not None}

        input = self._convert_messages_to_prompt(prompt)

        if config.stream:
            output_stream = self.client.chat.completions.create(
                messages=input,
                **filter_kwargs(self.client.chat.completions.create, all_kwargs),
            )

            return Stream(
                iterator=output_stream,
                kwargs=self._get_log_kwargs(prompt, None, **all_kwargs),
                processor=_process_chunk,
            )
        else:
            output = self.client.chat.completions.create(
                messages=input,
                **filter_kwargs(self.client.chat.completions.create, all_kwargs),
            )

            if config._log:
                self.log(
                    prompt=prompt,
                    response=OpenAIResponse(output),
                    **all_kwargs,
                )
                # Todo: set config= as param

        return OpenAIResponse(output)
