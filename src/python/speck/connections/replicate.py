import replicate

from ..chat.entities import IChatClient, IChatConfig, Prompt, Response, Stream
from .connector import IConnector
from .providers import Providers


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
        temperature: float = 1.0,
        test: bool = False,
        **config_kwargs
    ) -> Response | Stream:
        all_kwargs = {**config_kwargs, "temperature": temperature, "test": test}

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
            input={"prompt": input},
        )

        if stream:
            return Stream(
                iterator=output,
                kwargs=self._get_log_kwargs(prompt, model, None, **all_kwargs),
            )
        else:
            content = "".join(item for item in output)

            self.log(
                prompt=prompt,
                model=model,
                response=Response(content=content),
                **all_kwargs,
            )

            return Response(content=content)
