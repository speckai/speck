from typing import Union

from .chat.entities import ChatConfig, Prompt, Response
from .connections.anthropic import AnthropicConnector
from .connections.openai import OpenAIConnector
from .connections.openai_azure import AzureOpenAIConnector
from .connections.replicate import ReplicateConnector


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

    def create(self, *, prompt: Prompt, config: ChatConfig = None, **config_kwargs):
        if config is None:
            config = ChatConfig(**config_kwargs)
            # Todo: convert to default config based on class param

        if config.provider == None:
            # Try to extract provider by getting string before : in model
            if ":" in config.model:
                provider_str, model_str = config.model.split(":", 1)
                config.provider = provider_str
                config.model = model_str
            else:
                raise ValueError(
                    "Provider must be specified in config or as a class param"
                )

        if config.provider == "openai":
            connector = OpenAIConnector(api_key=self.client.api_keys["openai"].strip())
            return connector.chat(prompt, config, **config_kwargs)
        if config.provider == "azure-openai":
            connector = AzureOpenAIConnector(
                api_key=self.client.api_keys["azure-openai"].strip(),
                **self.client.azure_openai_config
            )
            return connector.chat(prompt, config, **config_kwargs)
        if config.provider == "replicate":
            connector = ReplicateConnector(
                api_key=self.client.api_keys["replicate"].strip()
            )
            return connector.chat(prompt, config, **config_kwargs)
        if config.provider == "anthropic":
            connector = AnthropicConnector(
                api_key=self.client.api_keys["anthropic"].strip()
            )
            return connector.chat(prompt, config, **config_kwargs)
        raise ValueError("Provider not found")

    def log(self, messages: Prompt, config: ChatConfig, response: Response):
        config.log_chat(messages, response)


class AsyncChat(AsyncResource):
    def __init__(self, client: "AsyncSpeck"):
        self.client = client

    def log(self, messages: Prompt, config: ChatConfig, response: Response):
        config.log_chat(messages, response)


class Speck(BaseClient):
    api_key: Union[str, None] = None
    api_keys: dict[str, str] = {}

    def __init__(self, api_key: Union[str, None] = None, api_keys: dict[str, str] = {}):
        self.api_key = api_key
        self.api_keys = api_keys
        self.azure_openai_config = {}
        self.chat = Chat(self)

    def add_api_key(self, provider: str, api_key: str):
        self.api_keys[provider] = api_key

    def add_azure_openai_config(self, azure_endpoint: str, api_version: str):
        self.azure_openai_config = {
            "azure_endpoint": azure_endpoint,
            "api_version": api_version,
        }


class AsyncSpeck(BaseClient):
    api_key: Union[str, None] = None

    def __init__(self, api_key: Union[str, None] = None):
        self.api_key = api_key
        self.chat = AsyncChat(self)


Client = Speck
AsyncClient = AsyncSpeck
