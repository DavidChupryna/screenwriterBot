import logging

import requests
from config import config

logging.basicConfig(
    level=config['LOGGING']['level'],
    format=config['LOGGING']['format'],
    filename=config['LOGGING']['filename'],
    filemode=config['LOGGING']['filemod']
)

MODEL_URI = f'gpt://{config['GPT']['FOLDER_ID']}/yandexgpt-lite'
headers = {
    'Authorization': f'Bearer {config['GPT']['IAM_TOKEN']}',
    'Content-Typy': 'application/json'}


def create_user_prompt(character, world, genre):
    prompt = (f'Напиши историю в стиле {genre}, где в главноей роли {character},'
               f' а сюжет развиваентся на планете {world}.'
               f' Начало должно быть коротким, 1-3 предложения.')
    return prompt


def create_prompt(user_id, user_data, user_prompt):
    prompt = config['PROMPTS']['SYSTEM']
    prompt += user_prompt
    if user_data[user_id]['additional_task']:
        prompt += f"Также учти пожелания пользователя {user_data[user_id]['additional_task']}"
    return prompt


def create_messages(params, prompt, answer):
    messages = []
    if params == 'Генерировать историю!':
        messages = [
            {
                'role': 'user',
                'text': prompt + config['PROMPTS']['CONTINUE']
            }
        ]
    elif params == 'Продолжить историю!':
        messages = [
            {
                'role': 'user',
                'text': prompt + config['PROMPTS']['CONTINUE']
            },
            {
                'role': 'assistant',
                'text': answer
            }
        ]
    elif params == 'Конец истории!':
        messages = [
            {
                'role': 'user',
                'text': prompt + config['PROMPTS']['END']
            },
            {
                'role': 'assistant',
                'text': answer
            }
        ]
    else:
        messages = [
            {
                'role': 'user',
                'text': prompt + config['PROMPTS']['CONTINUE'] + params
            },
            {
                'role': 'assistant',
                'text': answer
            }
        ]

    return messages


def count_tokens_in_session(messages):
    data = {
        "modelUri": MODEL_URI,
        "maxTokens": int(config['GPT']['MAX_TOKENS']),
        'messages': messages
    }
    return len(
        requests.post(
            config['GPT']['TOKENIZE_URL'],
            json=data,
            headers=headers
        ).json()["tokens"]
    )


def create_data(messages):
    json = {
        "modelUri": MODEL_URI,
        "completionOptions": {
            "stream": False,
            "temperature": config['GPT']['TEMPERATURE'],
            "maxTokens": int(config['GPT']['MAX_TOKENS'])
        },
        "messages": messages
    }
    return json


def send_request(ready_messages):
    used_tokens = count_tokens_in_session(ready_messages)
    try:
        resp = requests.post(
            url=config['GPT']['URL'],
            headers=headers,
            json=create_data(ready_messages))
        if resp.status_code != 200:
            return f'status code {resp.status_code}'
        message = resp.json()["result"]["alternatives"][0]["message"]['text']
        result = {
            'message': message,
            'used_token': used_tokens
        }
        return result

    except Exception as e:
        print("gpt error", e)