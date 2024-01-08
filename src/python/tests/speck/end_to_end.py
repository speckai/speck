from _load import generate_client
from speck import Message, Prompt, Response, Speck, Stream

client = generate_client(Speck, prod=False, debug=False)

models = [
    "openai:gpt-3.5-turbo",
    "anthropic:claude-2",
    "replicate:meta/llama-2-13b-chat:f4e2de70d66816a838a89eeeb621910adffb0dd0baba3976c96980970978018d",
]

for stream in [False, True]:
    print(f"Testing Models: ({stream and 'stream' or 'object'})")
    for model in models:
        print(f"Model: {model}")
        response: Stream = client.chat.create(
            prompt=Prompt(
                messages=[
                    Message(
                        role="system",
                        content="You are required to respond with CSV format.",
                    ),
                    Message(
                        role="user",
                        content="Count to 12.",
                    ),
                ],
            ),
            model=model,
            temperature=0.0,
            max_tokens=30,
            stream=stream,
            _log=True,
        )

        if stream:
            for r in response:
                print(r.content or "", end="", flush=True)

            print()
        else:
            print(response)

    print("\n\n" + "=" * 40 + "\n")
