from typing import Any, Literal

from pydantic import BaseModel

MessageRole = Literal["system", "user", "assistant"]


class Message(BaseModel):
    role: MessageRole
    content: str


class Messages(BaseModel):
    messages: list[Message]

    def __str__(self):
        return "\n".join([f"{message.role}: {message.content}" for message in self.messages])
