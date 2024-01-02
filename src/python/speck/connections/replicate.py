"""
Name: Replicate
URL: https://replicate.com/
Features:
- Chat
"""
from typing import Union

import replicate

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
        client: "Speck" = None,
        api_key: Union[str, None] = None,
        message_prefix: str = "<|im_start|>{role}\n",
        message_suffix: str = "<|im_end|>\n",
        messages_end: str = "<|im_start|>assistant\n",
    ):
        # Todo: support custom replicate model mappings
        # By default, built for meta/llama-2-70b
        super().__init__(client=client, provider=Providers.Replicate)
        self.api_key = api_key
        self.message_prefix = message_prefix
        self.message_suffix = message_suffix
        self.messages_end = messages_end

    def _convert_messages_to_prompt(self, messages: Prompt) -> list[dict[str, str]]:
        # Return tuple of system_prompt, prompt
        system_prompt = next(
            msg.content for msg in messages.messages if msg.role == "system"
        )
        prompt = "".join(
            msg.content for msg in messages.messages if msg.role != "system"
        )
        return system_prompt, prompt

    def chat(
        self, prompt: Prompt, config: ChatConfig = NOT_GIVEN, **config_kwargs
    ) -> Union[Response, Stream]:
        # all_kwargs = {
        #     **config_kwargs,
        #     "temperature": max(temperature, 0.01) if temperature is not None else None,
        #     "max_new_tokens": max_tokens,
        #     "top_p": top_p,
        #     "repetition_penalty": max(presence_penalty, 0.01)
        #     if presence_penalty
        #     else None,
        #     "top_k": top_k,
        #     "test": test,
        # }
        mapped_args = {
            "repetition_penalty": "presence_penalty",
        }
        all_kwargs = {
            mapped_args.get(k, k): v for k, v in vars(config).items() if v is not None
        }
        if all_kwargs.get("temperature") < 0.01:
            all_kwargs["temperature"] = 0.01

        # input = (
        #     "".join(
        #         self.message_prefix.format(role=msg.role)
        #         + msg.content
        #         + self.message_suffix.format(role=msg.role)
        #         for msg in prompt.messages
        #     )
        #     + self.messages_end
        # )
        system_prompt, user_prompt = self._convert_messages_to_prompt(prompt)
        config_kwargs["system_prompt"] = system_prompt

        output = replicate.run(
            config.model,
            input={"prompt": user_prompt, **all_kwargs},
        )

        if config.stream:
            return Stream(
                iterator=output,
                kwargs=self._get_log_kwargs(prompt, None, **all_kwargs),
                processor=_process_chunk,
            )
        else:
            content = "".join(item for item in output)

            if config._log:
                self.log(
                    prompt=prompt,
                    response=Response(content=content),
                    **all_kwargs,
                )

            return Response(content=content)
