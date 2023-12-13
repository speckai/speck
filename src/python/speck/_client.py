from . import Prompt


class Chat:
    def __init__(self, client: "Client"):
        self.client = client

    def log(self, messages: Prompt, response: str):
        pass


class Client:
    api_key: str | None = None

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.chat = Chat(self)
