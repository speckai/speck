from openai import ChatCompletion, OpenAI

from speck import chat

params = {
    "model": "gpt-4",
    "messages": [
        {"role": "system", "content": "hi"},
        {"role": "user", "content": "lol"},
    ],
}

client = OpenAI(api_key="")
response: ChatCompletion = client.chat.completions.create(**params)

print(response.model_dump())
chat.log(completion=response.model_dump(), **params)
