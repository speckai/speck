import replicate

from ..chat.entities import Messages
from .entities import IConnector, Models


class ReplicateConnector(IConnector):
    """
    https://replicate.com/
    """

    def __init__(
        self,
        message_prefix: str = "<|im_start|>{role}\n",
        message_suffix: str = "<|im_end|>\n",
        messages_end: str = "<|im_start|>assistant\n",
    ):
        self.message_prefix = message_prefix
        self.message_suffix = message_suffix
        self.messages_end = messages_end

    def process_message(self, messages: Messages, model: Models) -> str:
        input = (
            "".join(
                self.message_prefix.format(role=msg.role)
                + msg.content
                + self.message_suffix.format(role=msg.role)
                for msg in messages.messages
            )
            + self.messages_end
        )
        output = replicate.run(
            "01-ai/yi-34b-chat:914692bbe8a8e2b91a4e44203e70d170c9c5ccc1359b283c84b0ec8d47819a46",
            input={"prompt": input},
        )
        return "".join(item for item in output)
