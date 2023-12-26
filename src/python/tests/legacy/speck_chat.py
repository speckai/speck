# Import 2 levels up for speck
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import os

with open("../.env") as f:
    lines = f.readlines()
    for line in lines:
        key, value = line.split("=")
        os.environ[key] = value

from speck import ChatClient, Message, Prompt, Stream
from speck.chat.client import Providers

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
REPLICATE_API_TOKEN = os.getenv("REPLICATE_API_TOKEN")
print("OpenAI: ", OPENAI_API_KEY)
print("Replicate: ", REPLICATE_API_TOKEN)


# openai_client = Client(
#     provider=Providers.OpenAI,
#     provider_config={"api_key": "your_api_key"},
# )
# custom_client = Client(
#     provider=Providers.CustomProvider,
#     provider_config={"message_prefix": "Hello, ", "message_suffix": "!"},
# )
# print(openai_client)
# print(custom_client)

clients = [
    ChatClient.from_openai(api_key=OPENAI_API_KEY),
    # ChatClient.from_replicate(),
]

for client in clients:
    print(client)
    response: Stream = client.chat(
        Prompt(
            messages=[
                Message(role="system", content="You respond with 1 word answers."),
                Message(
                    role="user",
                    content="Respond with YES or NO. Do you understand? Then, recite the A B Cs",
                ),
            ],
        ),
        model="gpt-3.5-turbo",
        temperature=0.0,
        stream=True,
        _log=True,
    )
    # print(response)
    # print(next(response))
    # response.close()
    for r in response:
        print(r)
    print("=" * 10 + "\n" * 2)
