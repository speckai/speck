from typing import Union

from speck import Message

MessagesType = Union[str, Message, list[Message], list[dict[str, str]]]
