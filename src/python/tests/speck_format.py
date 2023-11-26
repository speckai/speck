from speck import Client
from speck.chat.client import Models, Providers

client = Client(provider=Providers.OpenAI, model=Models.GPT4)
print(client)
response = client.process_message("Hello, world!")
print(response)
