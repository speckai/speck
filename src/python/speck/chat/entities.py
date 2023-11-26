from pydantic import BaseModel


class Message(BaseModel):
    role: str
    content: str


class Messages(BaseModel):
    messages: list[Message]
