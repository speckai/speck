# Import 2 levels up for speck
import os
import sys

sys.path.append((os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

from speck import Message, Prompt, Speck, Stream

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

with open(".env") as f:
    lines = f.readlines()
    for line in lines:
        key, value = line.split("=")
        os.environ[key] = value


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
REPLICATE_API_TOKEN = os.getenv("REPLICATE_API_TOKEN")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
SPECK_API_KEY = os.getenv("SPECK_API_KEY")
print(SPECK_API_KEY)

client = Speck(
    api_key=SPECK_API_KEY,
    api_keys={
        # "openai": OPENAI_API_KEY,
        "replicate": REPLICATE_API_TOKEN,
        "azure_openai": AZURE_OPENAI_API_KEY,
        "anthropic": ANTHROPIC_API_KEY,
    },
)
client.add_azure_openai_config("", "")

response: Stream = client.chat.create(
    prompt=Prompt(
        messages=[
            Message(role="system", content="You respond with 1 word answers."),
            Message(
                role="user",
                content="Respond with YES or NO. Do you understand? Then, recite the A B Cs",
            ),
        ],
    ),
    model="anthropic:claude-2",
    # model="replicate:meta/llama-2-70b-chat:02e509c789964a7ea8736978a43525956ef40397be9033abf9fd2badfe68c9e3",
    temperature=0.0,
    stream=True,
    _log=True,
)

for r in response:
    print(r)

# print(response)