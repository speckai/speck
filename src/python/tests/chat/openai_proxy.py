from _load import OPENAI_API_KEY, SPECK_API_KEY
from speck import OpenAI

openai = OpenAI(api_key=OPENAI_API_KEY)
openai.add_speck_api_key(speck_api_key=SPECK_API_KEY)

kwargs = {
    "model": "gpt-3.5-turbo",
    "messages": [
        {"role": "system", "content": "hi"},
        {"role": "user", "content": "hi"},
    ],
}

response = openai.chat.completions.create(**kwargs, stream=False)
print(response)
