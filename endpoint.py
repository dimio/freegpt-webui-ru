import time
import json
import random
import time
from gevent import pywsgi
import socket

from g4f.Provider import (
    Aitianhu,
    Xiaor,
    You,
    Bing,
    Yqcloud,
    Theb,
    Bard,
    Vercel,
    Forefront,
    Lockchat,
    Liaobots,
    H2o,
    ChatgptLogin,
    DeepAi,
    GetGpt,
    Pierangelo,
    Gravityengine,
    ChatgptAi,
    ChatgptLogin,
    Phind,
    Easychat,
    hteyun,
    Weuseing,
    Fakeopen,
    Better,
    Alpha,
    Nino,
    Lsdev,
    Xiaor,
    Jayshen,
    Aws,
    DFEHub,
    Acytoo
)

from flask import Flask, request
from flask_cors import CORS

from g4f import ChatCompletion, Provider, Model

app = Flask(__name__)
CORS(app)

providers = [
    Aitianhu,
    Xiaor,
    #You,
    Bing,
    Yqcloud,
  #  Theb,
  #  Bard,
 #   Vercel,
  #  Forefront,
 #   Lockchat,
    Liaobots,
  #  H2o,
    ChatgptLogin,
    DeepAi,
    GetGpt,
    Pierangelo,
   # Gravityengine,
   # ChatgptAi,
   # ChatgptLogin,
    Phind,
    Easychat,
   # hteyun,
   # Weuseing,
   # Fakeopen,
    Better,
    Alpha,
    #Nino,
    Lsdev,
    #Xiaor,
    Jayshen,
    Aws,
    DFEHub,
    Acytoo
]


def get_working_provider(model, streaming):
    for provider in providers:
        try:
            ChatCompletion.create(model=model, stream=streaming, messages=[
                                     {"role": "user", "content": "Привет!"}], provider=provider)
            return provider
        except Exception:
            continue

    return None


provider = DFEHub
model_name = 'gpt-3.5-turbo'

@app.route("/v1/models", methods=['GET'])
def models():
    data = [
        {
            "id": "gpt-3.5-turbo",
            "object": "model",
            "owned_by": "organization-owner",
            "permission": []
        }
    ]
    return {'data': data, 'object': 'list'}
@app.route("/chat/completions", methods=['POST'])
@app.route("/v1/chat/completions", methods=['POST'])
@app.route("/", methods=['POST'])
def chat_completions():
    global provider
    streaming = request.json.get('stream', False)
    print(request.json) # не будем выводить клиентам, оставим для дебага
    model = request.json.get('model')
    messages = request.json.get('messages')

    try:
        response = ChatCompletion.create(model=model, stream=streaming, messages=messages, provider=provider)
    except:
        provider = get_working_provider(model, request.json.get('stream', False))
        if provider is None:
            # Если нет работающего провайдера, возвращаем ошибку
            raise Exception('No working provider available')
        response = ChatCompletion.create(model=model, stream=streaming, messages=messages, provider=provider)
    if not streaming:
        while 'curl_cffi.requests.errors.RequestsError' in response:
            try:
                response = ChatCompletion.create(model=model, stream=streaming, messages=messages, provider=provider)
            except:
                provider = get_working_provider(model, request.json.get('stream', False))
                if provider is None:
                    # Если нет работающего провайдера, возвращаем ошибку
                    raise Exception('No working provider available')
                response = ChatCompletion.create(model=model, stream=streaming, messages=messages, provider=provider)

        completion_timestamp = int(time.time())
        completion_id = ''.join(random.choices(
            'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789', k=28))

        return {
            'id': 'chatcmpl-%s' % completion_id,
            'object': 'chat.completion',
            'created': completion_timestamp,
            'model': model,
            'usage': {
                'prompt_tokens': 0,
                'completion_tokens': 0,
                'total_tokens': 0
            },
            'choices': [{
                'message': {
                    'role': 'assistant',
                    'content': response
                },
                'finish_reason': 'stop',
                'index': 0
            }]
        }

    def stream():
        completion_data = {
            'id': '',
            'object': 'chat.completion.chunk',
            'created': 0,
            'model': 'gpt-3.5-turbo-0301',
            'choices': [
                {
                    'delta': {
                        'content': ""
                    },
                    'index': 0,
                    'finish_reason': None
                }
            ]
        }

        for token in response:
            completion_id = ''.join(
                random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789', k=28))
            completion_timestamp = int(time.time())
            completion_data['id'] = f'chatcmpl-{completion_id}'
            completion_data['created'] = completion_timestamp
            completion_data['choices'][0]['delta']['content'] = token
            if token.startswith("an error occured"):
                completion_data['choices'][0]['delta']['content'] = "Server Response Error, please try again.\n"
                completion_data['choices'][0]['delta']['stop'] = "error"
                yield 'data: %s\n\ndata: [DONE]\n\n' % json.dumps(completion_data, separators=(',' ':'))
                return
            yield 'data: %s\n\n' % json.dumps(completion_data, separators=(',' ':'))
            time.sleep(0.1)

        completion_data['choices'][0]['finish_reason'] = "stop"
        completion_data['choices'][0]['delta']['content'] = ""
        yield 'data: %s\n\n' % json.dumps(completion_data, separators=(',' ':'))
        yield 'data: [DONE]\n\n'

    return app.response_class(stream(), mimetype='text/event-stream')


if __name__ == '__main__':
    site_config = {
        'host': '0.0.0.0',
        'port': 1337,
        'debug': True
    }

    
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)

    # Run the Flask server by WSGI
    print(f"Running on http://127.0.0.1:{site_config['port']}")
    print(f"Running on http://{ip_address}:{site_config['port']}")

    server = pywsgi.WSGIServer(('0.0.0.0', site_config['port']), app)
    server.serve_forever()

    print(f"Closing {ip_address}:{site_config['port']}")