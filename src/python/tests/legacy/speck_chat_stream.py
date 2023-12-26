from openai import OpenAI
from openai.types.chat import ChatCompletion

params = {
    "model": "gpt-4",
    "messages": [
        {"role": "system", "content": "You recite the alphabet.."},
        {"role": "user", "content": "Say your A B Cs"},
    ],
    "temperature": 1,
}

client = OpenAI(api_key="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")
response: ChatCompletion = client.chat.completions.create(**params, stream=True)


for chunk in response:
    print(chunk)
