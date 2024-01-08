from typing import Tuple, Union

from .chat.client import IChatClient
from .chat.entities import (ChatConfig, ChatConfigTypes, LogConfig, Prompt,
                            PromptTypes, Response, ResponseTypes)
from .connections.anthropic import AnthropicConnector
from .connections.openai import OpenAIConnector
from .connections.openai_azure import AzureOpenAIConnector
from .connections.replicate import ReplicateConnector
from .logs.app import app


# Todo: Add BaseClient
# Todo: Add AsyncResource, SyncResource
class BaseClient:
    api_key: Union[str, None]
    api_keys: dict[str, str]
    endpoint: Union[str, None]
    azure_openai_config: dict[str, str]
    debug: bool = False

    def add_api_key(self, provider: str, api_key: str):
        self.api_keys[provider] = api_key

    def add_azure_openai_config(self, azure_endpoint: str, api_version: str):
        self.azure_openai_config = {
            "azure_endpoint": azure_endpoint,
            "api_version": api_version,
        }

    def to_dict(self):
        return {
            "api_key": self.api_key,
            "api_keys": self.api_keys,
            "endpoint": self.endpoint,
            "azure_openai_config": self.azure_openai_config,
            "debug": self.debug,
        }


class Resource:
    pass


class AsyncResource(Resource):
    pass


class SyncResource(Resource):
    pass


class Logger(SyncResource):  # App logger
    def __init__(self, client: BaseClient):
        self.client = client

    def log(self, *args, **kwargs):
        kwargs["endpoint"] = self.client.endpoint
        app.log(*args, **kwargs)

    def info(self, *args, **kwargs):
        kwargs["endpoint"] = self.client.endpoint
        app.info(*args, **kwargs)

    def debug(self, *args, **kwargs):
        kwargs["endpoint"] = self.client.endpoint
        app.debug(*args, **kwargs)

    def warning(self, *args, **kwargs):
        kwargs["endpoint"] = self.client.endpoint
        app.warning(*args, **kwargs)

    def error(self, *args, **kwargs):
        kwargs["endpoint"] = self.client.endpoint
        app.error(*args, **kwargs)

    def critical(self, *args, **kwargs):
        kwargs["endpoint"] = self.client.endpoint
        app.critical(*args, **kwargs)

    def exception(self, *args, **kwargs):
        kwargs["endpoint"] = self.client.endpoint
        app.exception(*args, **kwargs)


def _create_connector(
    client: BaseClient, prompt: PromptTypes, config: ChatConfig = None, **config_kwargs
) -> IChatClient:
    if config is None:
        config = ChatConfig(**config_kwargs)
        # Todo: convert to default config based on class param
    elif len(config_kwargs) > 0:
        # Set config_kwargs as config attributes
        for key, value in config_kwargs.items():
            setattr(config, key, value)

    if config.provider is None:
        # Try to extract provider by getting string before : in model
        if ":" in config.model:
            provider_str, model_str = config.model.split(":", 1)
            config.provider = provider_str
            config.model = model_str
        else:
            raise ValueError("Provider must be specified in config or as a class param")

    if client.api_keys.get(config.provider) is None:
        raise ValueError(f"An API key for {config.provider} is required")

    client.log_config: LogConfig = None
    if client.api_key:
        log_config = LogConfig(
            api_key=client.api_key, endpoint=client.endpoint or "https://api.getspeck.ai"
        )
        client.log_config = log_config

    if config.provider == "openai":
        connector = OpenAIConnector(
            client=client,
            api_key=client.api_keys["openai"].strip(),
        )
        return connector
    if config.provider == "azure-openai":
        connector = AzureOpenAIConnector(
            client=client,
            api_key=client.api_keys["azure-openai"].strip(),
            **client.azure_openai_config,
        )
        return connector
    if config.provider == "replicate":
        connector = ReplicateConnector(
            client=client,
            api_key=client.api_keys["replicate"].strip(),
        )
        return connector
    if config.provider == "anthropic":
        connector = AnthropicConnector(
            client=client,
            api_key=client.api_keys["anthropic"].strip(),
        )
        return connector
    raise ValueError("Provider not found")


class Chat(SyncResource):
    def __init__(self, client: BaseClient):
        self.client = client

    def create(
        self, *, prompt: PromptTypes, config: ChatConfig = None, **config_kwargs
    ):
        prompt = Prompt.create(prompt)
        config = ChatConfig.create(config, config_kwargs)
        connector = _create_connector(self.client, prompt, config)

        if self.client.debug:
            # Create a socket connection to the server
            prompt, config = connector.debug_chat(prompt, config)
            config_kwargs = {}  # Converted in ChatConfig.create

        return connector.chat(prompt=prompt, config=config, **config_kwargs)

    def log(
        self, messages: PromptTypes, config: ChatConfigTypes, response: ResponseTypes
    ):
        prompt = Prompt.create(messages)
        config = ChatConfig.create(config)
        response = Response.create(response)
        config.log_chat(endpoint=self.client.endpoint, prompt=prompt, response=response)


class AsyncChat(AsyncResource):
    def __init__(self, client: BaseClient):
        self.client = client

    async def create(
        self, *, prompt: PromptTypes, config: ChatConfig = None, **config_kwargs
    ):
        prompt = Prompt.create(prompt)
        config = ChatConfig.create(config, config_kwargs)
        connector = _create_connector(self.client, prompt, config)
        return await connector.achat(prompt, config, **config_kwargs)

    def log(
        self,
        log_config: LogConfig,
        messages: Prompt,
        config: ChatConfig,
        response: Response,
    ):
        config.log_chat(log_config, prompt=messages, response=response)


class Speck(BaseClient):
    def __init__(
        self,
        api_key: Union[str, None] = None,
        api_keys: dict[str, str] = {},
        endpoint: str = "https://api.getspeck.ai",
        debug: bool = False,
    ):
        self.api_key = api_key.strip() if api_key is not None else None
        self.api_keys = api_keys
        self.endpoint = endpoint
        self.azure_openai_config = {}
        self.debug = debug

        self.chat = Chat(self)
        self.logger = Logger(self)


class AsyncSpeck(BaseClient):
    def __init__(
        self,
        api_key: Union[str, None] = None,
        api_keys: dict[str, str] = {},
        endpoint: Union[str, None] = "https://api.getspeck.ai",
        debug: bool = False,
    ):
        self.api_key = api_key.strip() if api_key is not None else None
        self.api_keys = api_keys
        self.endpoint = endpoint
        self.azure_openai_config = {}
        self.debug = debug

        self.chat = AsyncChat(self)
        self.logger = Logger(self)


Client = Speck
AsyncClient = AsyncSpeck
