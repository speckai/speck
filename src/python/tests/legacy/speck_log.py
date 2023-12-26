# Import 2 levels up for speck
import os
import sys

from openai import ChatCompletion, OpenAI

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from speck import chat, logger

params = {
    "model": "gpt-4",
    "messages": [
        {"role": "system", "content": "You are an assistant."},
        {"role": "user", "content": "What is my name?"},
    ],
    "temperature": 1,
}

client = OpenAI(api_key="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")
response: ChatCompletion = client.chat.completions.create(**params)
# logger.openai.log(response, **params)
# logger.app.log("Testing 12")
# logger.openai.log_verbose(completion=response.model_dump(), **params)
