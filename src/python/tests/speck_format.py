from speck import Client, Message, Messages
from speck.chat.client import Providers
from speck.connections.replicate import ReplicateConfig

openai_client = Client(
    provider=Providers.OpenAI,
    provider_config={"api_key": "your_api_key"},
)
custom_client = Client(
    provider=Providers.CustomProvider,
    provider_config={"message_prefix": "Hello, ", "message_suffix": "!"},
)

print(openai_client)
print(custom_client)

client = Client.from_openai(api_key="")
# client = Client.from_replicate()

print(client)
response = client.chat(
    Messages(
        messages=[
            Message(role="system", content="You respond with 1 word answers."),
            Message(role="user", content="Respond with YES or NO. Do you understand?"),
        ],
    ),
    model="gpt-3.5-turbo",
    temperature=0.0,
)
print(response)
