from .chat.entities import ChatConfig, Prompt, Response


class Chat:
    def __init__(self, client: "Speck"):
        self.client = client

    def log(self, messages: Prompt, config: ChatConfig, response: Response):
        config.log_chat(messages, response)


class Speck:
    api_key: str | None = None

    def __init__(self, api_key: str | None = None):
        self.api_key = api_key
        self.chat = Chat(self)


Client = Speck
