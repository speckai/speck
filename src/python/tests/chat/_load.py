# Import 2 levels up for speck
import os
import sys

sys.path.append(
    (os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
)

from speck import AsyncSpeck, Message, Prompt, Response, Speck

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

with open(".env") as f:
    lines = f.readlines()
    for line in lines:
        key, value = line.split("=")
        os.environ[key] = value.strip()


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
REPLICATE_API_TOKEN = os.getenv("REPLICATE_API_TOKEN")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
SPECK_API_KEY = os.getenv("SPECK_API_KEY")

client = Speck(
    api_key=SPECK_API_KEY,
    api_keys={
        "openai": OPENAI_API_KEY,
        "replicate": REPLICATE_API_TOKEN,
        "azure_openai": AZURE_OPENAI_API_KEY,
        "anthropic": ANTHROPIC_API_KEY,
    },
)
client.add_azure_openai_config("", "")

async_client = AsyncSpeck(
    api_key=SPECK_API_KEY,
    api_keys={
        "openai": OPENAI_API_KEY,
        "replicate": REPLICATE_API_TOKEN,
        "azure_openai": AZURE_OPENAI_API_KEY,
        "anthropic": ANTHROPIC_API_KEY,
    },
)
async_client.add_azure_openai_config("", "")
