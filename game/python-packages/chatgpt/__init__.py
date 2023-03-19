__version__ = "0.0.1"

import requests
import json

def completion(messages, api_key):
    url = "https://api.openai.com/v1/chat/completions"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    data = {
        "model": "gpt-3.5-turbo",
        "messages": messages
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        completion = response.json()["choices"][0]["message"]
        messages.append(completion)
        return messages
    else:
        raise Exception(f"Error: {response.status_code}, {response.text}")
