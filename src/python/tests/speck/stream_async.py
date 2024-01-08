import asyncio

from _load import generate_client
from speck import Message, Prompt, Response, Speck, Stream

client = generate_client(Speck, prod=False, debug=False)


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
