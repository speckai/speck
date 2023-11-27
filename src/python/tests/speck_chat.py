from speck import ChatClient, Message, Prompt
from speck.chat.client import Providers
from speck.connections.replicate import ReplicateConfig

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
        api_key="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"
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
                    role="user", content="Respond with YES or NO. Do you understand?"
                ),
            ],
        ),
        model="gpt-3.5-turbo",
        temperature=0.0,
        stream=True,
    )
    print(response)
    for r in response:
        print(r)
    print("=" * 10 + "\n" * 2)
