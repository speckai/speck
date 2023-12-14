import os

with open(".env") as f:
    lines = f.readlines()
    for line in lines:
        key, value = line.split("=")
        os.environ[key] = value

import os

from openai import AsyncOpenAI

client = AsyncOpenAI(api_key=os.environ["OPENAI_API_KEY"])

kwargs = {
    "model": "gpt-3.5-turbo",
    "messages": [
        {"role": "system", "content": "hi"},
        {"role": "user", "content": "hi"},
    ],
}

for stream in [False, True]:
    completion = await client.chat.completions.create(
        **kwargs,
        stream=stream,
    )

    if stream:
        for chunk in completion:
            print(chunk.choices[0].delta.content)
    else:
        print(completion.choices[0].message)
