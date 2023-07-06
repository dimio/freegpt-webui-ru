import requests
import os
import json
from ...typing import sha256, Dict, get_type_hints

url = 'https://8300q.aitianhu.top'
model = ['gpt-3.5-turbo']
supports_stream = True
needs_auth = False

def _create_completion(model: str, messages: list, stream: bool, temperature: float = 0.7, **kwargs):
    headers = {
        'Content-Type': 'application/json',
        'Origin':'https://8300q.aitianhu.top',
        'Referer':'https://8300q.aitianhu.top/'
    }
    data = {
        'model': model,
        'promt': messages,
        'systemMessage': "You are ChatGPT, a large language model trained by OpenAI. Follow the user's instructions carefully. Respond using markdown."
    }
    response = requests.post(url + '/api/chat-process', headers=headers,
                             json=data, stream=True)
    

    return response.json()['text']

params = f'g4f.Providers.{os.path.basename(__file__)[:-3]} supports: ' + \
    '(%s)' % ', '.join([f"{name}: {get_type_hints(_create_completion)[name].__name__}" for name in _create_completion.__code__.co_varnames[:_create_completion.__code__.co_argcount]])
