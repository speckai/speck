import os

with open(".env") as f:
    lines = f.readlines()
    for line in lines:
        key, value = line.split("=")
        os.environ[key] = value

import os

from openai import OpenAI
from speck import ChatConfig, Prompt, Response, Speck

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
speck = Speck(api_key=None)

kwargs = {
    "model": "gpt-3.5-turbo",
    "messages": [
        {"role": "system", "content": "hi"},
        {"role": "user", "content": "hi"},
    ],
}

completion = client.chat.completions.create(
    **kwargs,
    stream=False,
)

speck.chat.log(
    Prompt(kwargs["messages"]),
    ChatConfig(model=kwargs["model"]),
    Response(completion.choices[0].message.content),
)

print(completion.choices[0].message)
