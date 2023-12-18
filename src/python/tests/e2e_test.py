# Import 2 levels up for speck
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv

from speck import ChatClient, ChatConfig, Message, Prompt, Response, Stream

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
    ChatClient.from_openai(api_key=OPENAI_API_KEY),
    ChatClient.from_openai(api_key=OPENAI_API_KEY),
    # ChatClient.from_replicate(),
]

for idx, client in enumerate(clients):
    print(idx)
    response: Stream | Response = client.chat(
        Prompt(
            messages=[
                Message(role="system", content="You respond with 1 word answers."),
                Message(
                    role="user",
                    content="Respond with YES or NO. Do you understand? Then, recite the A B Cs",
                ),
            ],
        ),
        ChatConfig(
            model="gpt-3.5-turbo",
            temperature=0.0,
            stream=idx==1,
            _log=True,
        ),
    )

    if idx == 0:
        print(response)
        print(type(response))
    else:
        for chunk in response:
            print(chunk)
