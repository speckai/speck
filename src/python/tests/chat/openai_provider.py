from _load import ANTHROPIC_API_KEY, OPENAI_API_KEY, SPECK_API_KEY
from speck import OpenAI

openai = OpenAI(api_key=OPENAI_API_KEY)
openai.initialize_speck(
    speck_api_key=SPECK_API_KEY, api_keys={"anthropic": ANTHROPIC_API_KEY}
)

kwargs = {
    "model": "anthropic:claude-2",
    "messages": [
        {"role": "system", "content": "hi"},
        {"role": "user", "content": "hi"},
    ],
}

response = openai.chat.completions.create(**kwargs, stream=False)
print(response)
