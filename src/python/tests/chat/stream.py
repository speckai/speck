from _load import client
from speck import Message, Prompt, Response, Stream

models = [
    "openai:gpt-3.5-turbo",
    "anthropic:claude-2",
    "replicate:meta/llama-2-13b-chat:f4e2de70d66816a838a89eeeb621910adffb0dd0baba3976c96980970978018d",
]

for model in models:
    print(f"\n\n\nModel: {model}")
    response: Stream = client.chat.create(
        prompt=Prompt(
            messages=[
                Message(role="system", content="You respond with 1 word answers."),
                Message(
                    role="user",
                    content="Respond with YES or NO. Do you understand? Then, count to 10.",
                ),
            ],
        ),
        model=model,
        temperature=1.0,
        max_tokens=100,
        stream=True,
        _log=True,
    )

    for r in response:
        print(r.content or "", end="", flush=True)

    print()
    # print(response)
