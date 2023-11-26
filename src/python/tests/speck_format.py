from speck import Client, Message, Messages
from speck.chat.client import Providers
from speck.connections.entities import Models

openai_client = Client(
    provider=Providers.OpenAI,
    model=Models.GPT4,
    provider_config={"api_key": "your_api_key"},
)
custom_client = Client(
    provider=Providers.CustomProvider,
    model=Models.GPT4,
    provider_config={"message_prefix": "Hello, ", "message_suffix": "!"},
)

print(openai_client)
print(custom_client)

# client = Client.from_openai(api_key="")
client = Client.from_replicate()

print(client)
response = client.process_message(
    Messages(
        messages=[
            Message(role="system", content="You respond with 1 word answers."),
            Message(role="user", content="Respond with YES"),
        ],
    ),
    model=Models.GPT35_TURBO,
)
print(response)
