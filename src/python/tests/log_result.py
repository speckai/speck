import os

with open(".env") as f:
    lines = f.readlines()
    for line in lines:
        key, value = line.split("=")
        os.environ[key] = value

import os

from openai import OpenAI
from speck import Client

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
speck =

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

print(completion.choices[0].message)