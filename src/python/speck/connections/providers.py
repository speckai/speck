from enum import Enum


class Providers(Enum):
    OpenAI = "OpenAI"
    AzureOpenAI = "AzureOpenAI"
    CustomProvider = "CustomProvider"
    Replicate = "Replicate"
