import asyncio
import os
import sys

sys.path.append(
    (os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
)
from speck import AsyncSpeck, Message, Prompt, Response

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

client = AsyncSpeck(
    api_key=SPECK_API_KEY,
    api_keys={
        "openai": OPENAI_API_KEY,
        "replicate": REPLICATE_API_TOKEN,
        "azure_openai": AZURE_OPENAI_API_KEY,
        "anthropic": ANTHROPIC_API_KEY,
    },
)

client.add_azure_openai_config("", "")


async def main():
    response: Response = await client.chat.create(
        prompt=Prompt(
            messages=[
                Message(role="system", content="You respond with 1 word answers."),
                Message(
                    role="user",
                    content="Respond with YES or NO. Do you understand? Then, count to 500.",
                ),
            ],
        ),
        model="openai:gpt-3.5-turbo",
        # model="anthropic:claude-2",
        # model="replicate:meta/llama-2-70b-chat:02e509c789964a7ea8736978a43525956ef40397be9033abf9fd2badfe68c9e3",
        temperature=1.0,
        stream=False,
        _log=True,
    )

    print("Output:")
    # for r in response:
    #     print(r)
    print(response)


if __name__ == "__main__":
    asyncio.run(main())
