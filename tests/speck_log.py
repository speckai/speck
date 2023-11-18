from openai import ChatCompletion, OpenAI

from speck.llm import chat
from speck.logs import logger

params = {
    "model": "gpt-4",
    "messages": [
        {"role": "system", "content": "hi"},
        {"role": "user", "content": "Failed to work"},
        {"role": "assistant", "content": "What is the problem?"},
        {"role": "user", "content": "It doesn't work"},
    ],
    "temperature": 0.7,
}

client = OpenAI(api_key="")
response: ChatCompletion = client.chat.completions.create(**params)

print(response.model_dump())
chat.llm_log(completion=response.model_dump(), **params)
logger.app_log(message="hi")
