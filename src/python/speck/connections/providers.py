from enum import Enum


class Providers(Enum):
    Anthropic = "Anthropic"
    AzureOpenAI = "AzureOpenAI"
    OpenAI = "OpenAI"
    CustomProvider = "CustomProvider"
    Replicate = "Replicate"
