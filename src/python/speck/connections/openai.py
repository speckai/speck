"""
Name: OpenAI
URL: https://platform.openai.com/docs/api-reference
Features:
- Chat
- Vision
- Text-to-Speech
- Speech-to-Text
"""
from typing import Union

from openai import OpenAI
from openai.types.chat import ChatCompletion

from ..chat.entities import (
    NOT_GIVEN,
    ChatConfig,
    IChatClient,
    MessageChunk,
    Prompt,
    Response,
    Stream,
)
from ..util import filter_kwargs, get_dict
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
            raw=get_dict(chat_completion),
        )


class OpenAIConnector(IConnector, IChatClient):
    def __init__(
        self, client: "Speck" = None, api_key: str = None, speck_api_key: str = None
    ):
        super().__init__(
            client=client, provider=Providers.OpenAI, speck_api_key=speck_api_key
        )
        if api_key is not None:
            self.api_key = api_key
            self.client = OpenAI(api_key=self.api_key)

    def _convert_messages_to_prompt(self, messages: Prompt) -> list[dict[str, str]]:
        return [{"role": msg.role, "content": msg.content} for msg in messages.messages]

    def _process(
        self,
        prompt: Prompt,
        config: ChatConfig = NOT_GIVEN,
        _speck_async=False,
        **config_kwargs
    ) -> Union[OpenAIResponse, Stream]:
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
                client=self._client,
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

    def chat(
        self, prompt: Prompt, config: ChatConfig = NOT_GIVEN, **config_kwargs
    ) -> Union[OpenAIResponse, Stream]:
        return self._process(prompt, config, _speck_async=False, **config_kwargs)

    def achat(
        self, prompt: Prompt, config: ChatConfig = NOT_GIVEN, **config_kwargs
    ) -> Union[OpenAIResponse, Stream]:
        return self._process(prompt, config, _speck_async=True, **config_kwargs)
