"""
Name: OpenAI Azure
URL:
Features:
"""
from openai import AsyncAzureOpenAI, AzureOpenAI

from .openai import OpenAIConnector


class AzureOpenAIConnector(OpenAIConnector):
    def __init__(
        self,
        api_key: str,
        azure_endpoint: str,
        api_version: str,
        **kwargs
    ):
        super().__init__(api_key=None)
        self.client = AzureOpenAI(
            api_key=self.api_key,
            azure_endpoint=azure_endpoint,
            api_version=api_version,
            **kwargs
        )
        self.async_client = AsyncAzureOpenAI(
            api_key=self.api_key,
            azure_endpoint=azure_endpoint,
            api_version=api_version,
            **kwargs
        )
        self.api_key = api_key
        self.azure_endpoint = azure_endpoint
        self.api_version = api_version
