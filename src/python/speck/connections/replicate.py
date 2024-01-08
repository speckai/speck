"""
Name: Replicate
URL: https://replicate.com/
Features:
- Chat
"""
from typing import Union

import replicate
from replicate import Client

from ..chat.entities import (
    ChatConfig,
    IChatClient,
    LogConfig,
    MessageChunk,
    Prompt,
    Response,
    Stream,
)
from .connector import IConnector
from .providers import Providers

NOT_GIVEN = None


def _process_chunk(obj) -> MessageChunk:
    return MessageChunk(
        content=obj.data if str(obj.event) == "EventType.OUTPUT" else ""
    )


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
        self.replicate_client = Client(api_token=api_key)

    def _convert_messages_to_prompt(self, messages: Prompt) -> list[dict[str, str]]:
        # Return tuple of system_prompt, prompt
        system_prompt = next(
            msg.content for msg in messages.messages if msg.role == "system"
        )
        prompt = "".join(
            msg.content for msg in messages.messages if msg.role != "system"
        )
        return system_prompt, prompt

    def _process_args(self, prompt: Prompt, config: ChatConfig, **config_kwargs):
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
        blocked_kwargs = ["provider", "_log", "chat_args", "stream", "max_tokens"]
        mapped_args = {"repetition_penalty": "presence_penalty"}
        all_kwargs = {
            mapped_args.get(k, k): v
            for k, v in vars(config).items()
            if v is not None and k not in blocked_kwargs
        }
        if all_kwargs.get("temperature") < 0.01:
            all_kwargs["temperature"] = 0.01

        log_kwargs = {k: v for k, v in vars(config).items() if v is not None}

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
        all_kwargs["system_prompt"] = system_prompt

        # Remove unused kwargs (kept in, these values can cause errors)
        for arg in ["stream", "provider", "_log", "chat_args"]:
            if arg in all_kwargs:
                del all_kwargs[arg]

        log_config: LogConfig = None
        if config_kwargs.get("_log"):
            if self._client.log_config:
                log_config = self._client.log_config

            elif not config_kwargs.get("log_config"):
                raise ValueError(
                    "No log config found. Define the log config in the log or client."
                )
            else:
                log_config = config_kwargs.get("log_config")

        return system_prompt, user_prompt, all_kwargs, log_kwargs, log_config

    def chat(
        self, prompt: Prompt, config: ChatConfig = NOT_GIVEN, **config_kwargs
    ) -> Union[Response, Stream]:
        (
            system_prompt,
            user_prompt,
            all_kwargs,
            log_kwargs,
            log_config,
        ) = self._process_args(prompt, config, **config_kwargs)

        if config.stream:
            output = self.replicate_client.stream(
                config.model,
                input={"prompt": user_prompt, **all_kwargs},
            )

            return Stream(
                client=self._client,
                iterator=output,
                log_config=log_config,
                kwargs=self._get_log_kwargs(prompt, None, **log_kwargs),
                processor=_process_chunk,
            )
        else:
            output = self.replicate_client.run(
                config.model,
                input={"prompt": user_prompt, **all_kwargs},
            )

            content = "".join(output)

            if config._log:
                self.log(
                    log_config=log_config,
                    prompt=prompt,
                    response=Response(content=content),
                    **log_kwargs,
                )

            return Response(content=content)

    async def achat(
        self, prompt: Prompt, config: ChatConfig = NOT_GIVEN, **config_kwargs
    ) -> Union[Response, Stream]:
        (
            system_prompt,
            user_prompt,
            all_kwargs,
            log_kwargs,
            log_config,
        ) = self._process_args(prompt, config, **config_kwargs)

        if config.stream:
            output = await self.replicate_client.async_stream(
                config.model,
                input={"prompt": user_prompt, **all_kwargs},
            )

            return Stream(
                iterator=output,
                log_config=log_config,
                kwargs=self._get_log_kwargs(prompt, None, **log_kwargs),
                processor=_process_chunk,
            )
        else:
            output = await self.replicate_client.async_run(
                config.model,
                input={"prompt": user_prompt, **all_kwargs},
            )

            content = "".join(item for item in output)

            if config._log:
                self.log(
                    log_config=log_config,
                    prompt=prompt,
                    response=Response(content=content),
                    **log_kwargs,
                )

            return Response(content=content)
