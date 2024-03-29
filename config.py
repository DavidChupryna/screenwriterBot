import configparser

config = configparser.ConfigParser()
config['LOGGING'] = {
    'level': 'INFO',
    'format': '%%(asctime)s - %%(name)s - %%(levelname)s - %%(message)s',
    'filename': 'log_file.txt',
    'filemod': 'w'
    }

config['GPT'] = {
    'URL': 'https://llm.api.cloud.yandex.net/foundationModels/v1/completion',
    'IAM_TOKEN': 't1.9euelZqWlZWWx5mLl42NlZKZmJCSmO3rnpWay52RlYuSns_Hx8mZlYnNlZfl9Pd8UGRP-e8pJlGH3fT3PH9hT_nvKSZRh83n9euelZrNnJKakJLMys2PkMeUmpWYmu_8xeuelZrNnJKakJLMys2PkMeUmpWYmr3rnpWazcqLz5adzMzJipqMip6ck4613oac0ZyQko-Ki5rRi5nSnJCSj4qLmtKSmouem56LntKMng.orju17cwYHy9FmG0f6DD70Q-XjZh2HuwH7mYdwu_TdRSAvPFGx8mVKsLoM0sdZyv5pTbHVi-UiH63QR7Bi_2CQ',
    'TEMPERATURE': '0.6',
    'MAX_TOKENS': '64',
    'TOKENIZE_URL': 'https://llm.api.cloud.yandex.net/foundationModels/v1/tokenizeCompletion',
    'FOLDER_ID': 'b1gmco3nm6e4ud4orfv9'
    }

config['LIMITS'] = {
    'MAX_MESSAGE_TOKENS': '50',
    'MAX_USERS': '2',
    'MAX_SESSION': '3',
    'MAX_TOKEN_IN_SESSION': '1000',
    }

config['PROMPTS'] = {
    'SYSTEM': 'Ты пишешь историю по заданым пользователем параметрам. Начинает пользовватель, а ты продолжаешь.'
                    ' В историю можешь добавлять диалоги между пресонажами. Диалоги пиши с новой строки и отделяй тире.'
                    'В истории не приветствуется пояснительный текст.',
    'END': 'Напиши логическое завершение истории c неожиданной развязкой. Не добавляй пояснительный текст',
    'CONTINUE': 'Логически продолжи сюжет в 1-3 предложения, держи интригу. Не добавляй пояснительный текст'
}
bot_token = '7184586489:AAHavezhvXtnqkWqTXCzEGLN3efnL-y0BI4'
