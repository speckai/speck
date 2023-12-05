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
    IChatClient,
    IChatConfig,
    MessageChunk,
    Prompt,
    Response,
    Stream,
)
from .connector import IConnector
from .providers import Providers

OpenAIModel = Literal["gpt-4", "gpt-3.5", "gpt-3.5-turbo"]
NOT_GIVEN = None


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


class OpenAIChatConfig(IChatConfig):
    """
    NOT USED ANYMORE. REPLACED BY **kwargs
    """

    def __init__(self, temperature: float = 1.0, **kwargs):
        super().__init__(**kwargs)
        self.temperature = temperature


class OpenAIConnector(IConnector, IChatClient):
    def __init__(self, api_key: str):
        super().__init__(provider=Providers.OpenAI)
        self.api_key = api_key
        self.client = OpenAI(api_key=self.api_key)
        print(api_key)

    def _convert_messages_to_prompt(self, messages: Prompt) -> list[dict[str, str]]:
        return [{"role": msg.role, "content": msg.content} for msg in messages.messages]

    def chat(
        self,
        prompt: Prompt,
        model: OpenAIModel,
        stream: bool = False,
        _log: bool = True,
        temperature: Optional[float] | NotGiven = NOT_GIVEN,
        max_tokens: Optional[int] | NotGiven = NOT_GIVEN,
        top_p: Optional[float] | NotGiven = NOT_GIVEN,
        frequency_penalty: Optional[float] | NotGiven = NOT_GIVEN,
        presence_penalty: Optional[float] | NotGiven = NOT_GIVEN,
        **config_kwargs
    ) -> OpenAIResponse | Stream:
        all_kwargs = {
            **config_kwargs,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "top_p": top_p,
            "frequency_penalty": frequency_penalty,
            "presence_penalty": presence_penalty,
        }
        # Remove all None values
        all_kwargs = {k: v for k, v in all_kwargs.items() if v is not None}

        input = self._convert_messages_to_prompt(prompt)

        if stream:
            output_stream = self.client.chat.completions.create(
                messages=input,
                model=model,
                stream=True,
                **all_kwargs,
            )

            return Stream(
                iterator=output_stream,
                kwargs=self._get_log_kwargs(
                    prompt, model, None, _log=_log, **all_kwargs
                ),
                processor=_process_chunk,
            )
        else:
            output = self.client.chat.completions.create(
                messages=input,
                model=model,
                **all_kwargs,
            )

            if _log:
                self.log(
                    prompt=prompt,
                    model=model,
                    response=OpenAIResponse(output),
                    **all_kwargs,
                )

        return OpenAIResponse(output)
