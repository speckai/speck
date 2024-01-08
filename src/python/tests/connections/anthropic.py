import json

import requests


def call_anthropic_api():
    # API endpoint
    url = "https://api.anthropic.com/v1/complete"

    # Headers
    headers = {
        "anthropic-version": "2023-06-01",
        "content-type": "application/json",
        "x-api-key": "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",  # Replace with your actual API key
    }

    # Data payload
    data = {
        "model": "claude-2",
        "prompt": "\n\nHuman: Hello, world!\n\nAssistant:",
        "max_tokens_to_sample": 256,
        "stream": True,
    }

    # Making the POST request
    response = requests.post(url, headers=headers, data=json.dumps(data), stream=True)

    # Checking if the request was successful
    if response.status_code == 200:
        return response.json()
    else:
        return response.text


# Call the function
response = call_anthropic_api()
# print(response)
# for line in response:
#     print(line.decode("utf-8"))
