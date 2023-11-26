from speck import Client, Message, Messages
from speck.chat.client import Models, Providers

openai_client = Client(provider=Providers.OpenAI, model=Models.GPT4, provider_config={"api_key": "your_api_key"})
custom_client = Client(provider=Providers.CustomProvider, model=Models.GPT4, provider_config={"message_prefix": "Hello, ", "message_suffix": "!"})

print(openai_client)
print(custom_client)

client = Client(provider=Providers.OpenAI, model=Models.GPT4)
print(client)
response = client.process_message(Messages(
    messages=[
        Message(role="system", content="You exist."),
        Message(role="user", content="Hello, world!"),
    ]
))
print(response)
