from .chat.entities import ChatConfig, Prompt, Response


# Todo: Add BaseClient
# Todo: Add AsyncResource, SyncResource
class BaseClient:
    pass


class Resource:
    pass


class AsyncResource(Resource):
    pass


class SyncResource(Resource):
    pass


class Chat(SyncResource):
    def __init__(self, client: "Speck"):
        self.client = client

    def log(self, messages: Prompt, config: ChatConfig, response: Response):
        config.log_chat(messages, response)


class AsyncChat(AsyncResource):
    def __init__(self, client: "AsyncSpeck"):
        self.client = client

    def log(self, messages: Prompt, config: ChatConfig, response: Response):
        config.log_chat(messages, response)


class Speck(BaseClient):
    api_key: str | None = None

    def __init__(self, api_key: str | None = None):
        self.api_key = api_key
        self.chat = Chat(self)


class AsyncSpeck(BaseClient):
    api_key: str | None = None

    def __init__(self, api_key: str | None = None):
        self.api_key = api_key
        self.chat = AsyncChat(self)


Client = Speck
AsyncClient = AsyncSpeck
