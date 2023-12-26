# Import 2 levels up for speck
import os
import sys

from speck import Message, Prompt, Speck, Stream

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

with open("../.env") as f:
    lines = f.readlines()
    for line in lines:
        key, value = line.split("=")
        os.environ[key] = value


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
REPLICATE_API_TOKEN = os.getenv("REPLICATE_API_TOKEN")
print("OpenAI: ", OPENAI_API_KEY)
print("Replicate: ", REPLICATE_API_TOKEN)

client = Speck(
    api_key=None, api_keys={"openai": OPENAI_API_KEY, "replicate": REPLICATE_API_TOKEN}
)

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
    # model="openai:gpt-3.5-turbo",
    model="replicate:meta/llama-2-70b-chat:02e509c789964a7ea8736978a43525956ef40397be9033abf9fd2badfe68c9e3",
    temperature=0.0,
    stream=True,
    _log=True,
)

for r in response:
    print(r)
