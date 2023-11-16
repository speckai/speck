from openai import ChatCompletion, OpenAI

from speck import chat

params = {
    "model": "gpt-4",
    "messages": [
        {"role": "system", "content": "hi"},
        {"role": "user", "content": "Failed to work"},
        {"role": "assistant", "content": "What is the problem?"},
        {"role": "user", "content": "It doesn't work"},
        {"role": "assistant", "content": "What doesn't work?"},
        {"role": "user", "content": "Everything"},
        {"role": "assistant", "content": "What do you mean by everything?"},
        {"role": "user", "content": "I mean everything"},
        {"role": "assistant", "content": "I don't understand"},
        {"role": "user", "content": "I don't understand either"},
    ],
}

client = OpenAI(api_key="")
response: ChatCompletion = client.chat.completions.create(**params)

print(response.model_dump())
chat.log(completion=response.model_dump(), **params)
