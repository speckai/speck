"""
Name: Replicate
URL: https://replicate.com/
Features:
- Chat
"""
from typing import Optional

import replicate
from openai._types import NotGiven

from ..chat.entities import (
    ChatConfig,
    IChatClient,
    MessageChunk,
    Prompt,
    Response,
    Stream,
)
from .connector import IConnector
from .providers import Providers

NOT_GIVEN = None


def _process_chunk(obj) -> MessageChunk:
    return MessageChunk(content=obj)


class ReplicateConnector(IConnector, IChatClient):
    """
    https://replicate.com/
    """

    def __init__(
        self,
        api_key: str | None = None,
        message_prefix: str = "<|im_start|>{role}\n",
        message_suffix: str = "<|im_end|>\n",
        messages_end: str = "<|im_start|>assistant\n",
    ):
        super().__init__(provider=Providers.Replicate)
        self.api_key = api_key
        self.message_prefix = message_prefix
        self.message_suffix = message_suffix
        self.messages_end = messages_end

    def chat(
        self,
        prompt: Prompt,
        model: str,
        stream: bool = False,
        _log: bool = True,
        temperature: Optional[float] | NotGiven = NOT_GIVEN,
        max_tokens: Optional[int] | NotGiven = 10,
        top_p: Optional[float] | NotGiven = NOT_GIVEN,
        presence_penalty: Optional[float] | NotGiven = NOT_GIVEN,
        top_k: Optional[int] | NotGiven = NOT_GIVEN,
        test: bool = False,
        **config_kwargs
    ) -> Response | Stream:
        all_kwargs = {
            **config_kwargs,
            "temperature": max(temperature, 0.01) if temperature is not None else None,
            "max_new_tokens": max_tokens,
            "top_p": top_p,
            "repetition_penalty": max(presence_penalty, 0.01)
            if presence_penalty
            else None,
            "top_k": top_k,
            "test": test,
        }
        # Remove all None values
        all_kwargs = {k: v for k, v in all_kwargs.items() if v is not None}

        input = (
            "".join(
                self.message_prefix.format(role=msg.role)
                + msg.content
                + self.message_suffix.format(role=msg.role)
                for msg in prompt.messages
            )
            + self.messages_end
        )
        print(input)
        output = replicate.run(
            "01-ai/yi-34b-chat:914692bbe8a8e2b91a4e44203e70d170c9c5ccc1359b283c84b0ec8d47819a46",
            input={"prompt": input, **all_kwargs},
        )

        if stream:
            return Stream(
                iterator=output,
                kwargs=self._get_log_kwargs(prompt, None, _log=_log, **all_kwargs),
                processor=_process_chunk,
            )
        else:
            content = "".join(item for item in output)

            if _log:
                self.log(
                    prompt=prompt,
                    model=model,
                    response=Response(content=content),
                    **all_kwargs,
                )

            return Response(content=content)
