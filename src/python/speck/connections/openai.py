from typing import Literal

from openai import OpenAI
from openai.types.chat import ChatCompletion

from ..chat.entities import IChatClient, IChatConfig, Prompt, Response, Stream
from .connector import IConnector
from .providers import Providers

OpenAIModel = Literal["gpt-4", "gpt-3.5", "gpt-3.5-turbo"]


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
        temperature: float = 1.0,
        **config_kwargs
    ) -> OpenAIResponse | Stream:
        all_kwargs = {**config_kwargs, "temperature": temperature}

        input = self._convert_messages_to_prompt(prompt)

        if stream:
            output_stream = self.client.chat.completions.create(
                messages=input,
                model=model,
                temperature=temperature,
                stream=True,
                **config_kwargs,
            )

            return Stream(
                iterator=output_stream,
                kwargs=self._get_log_kwargs(prompt, model, None, **all_kwargs),
            )
        else:
            output = self.client.chat.completions.create(
                messages=input, model=model, temperature=temperature, **config_kwargs
            )

            self.log(
                prompt=prompt,
                model=model,
                response=OpenAIResponse(output),
                **all_kwargs,
            )

        return OpenAIResponse(output)
