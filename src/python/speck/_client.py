from . import Prompt


class Chat:
    def __init__(self, client: "Speck"):
        self.client = client

    def log(self, messages: Prompt, response: str):
        pass


class Speck:
    api_key: str | None = None

    def __init__(self, api_key: str | None = None):
        self.api_key = api_key
        self.chat = Chat(self)


Client = Speck
