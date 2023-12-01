# Import 2 levels up for speck
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from speck import ChatClient, Message, Prompt
from speck.chat.client import Providers

from dotenv import load_dotenv

load_dotenv()

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
    ChatClient.from_openai(
        api_key=OPENAI_API_KEY
    ),
    ChatClient.from_replicate(),
]

for client in clients:
    print(client)
    response = client.chat(
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
        # stream=True,
    )
    print(response)
    for r in response:
        print(r)
    print("=" * 10 + "\n" * 2)
