from enum import Enum


class Providers(Enum):
    Anthropic = "Anthropic"
    AzureOpenAI = "AzureOpenAI"
    OpenAI = "OpenAI"
    CustomProvider = "CustomProvider"
    Replicate = "Replicate"


ProvidersList: list[str] = []
for provider in Providers:
    ProvidersList.append(provider.value.lower())
