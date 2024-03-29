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
    'IAM_TOKEN': 't1.9euelZqdmp2enp7LnouPz5CSjpGOj-3rnpWay52RlYuSns_Hx8mZlYnNlZfl9PdwZWdP-e9QdRyc3fT3MBRlT_nvUHUcnM3n9euelZqPyMfHjJ6bmJ6Qys3NxpnGjO_8xeuelZqPyMfHjJ6bmJ6Qys3NxpnGjL3rnpWajJOKyZWeic6czcqRmoyJnpC13oac0ZyQko-Ki5rRi5nSnJCSj4qLmtKSmouem56LntKMng.D72mW4fdqqtZizuJ6Mzp-7L-23984a34DQ80i9IOf2BLwF_wiIJgCQHTQYJjUwsmQUTpTotX6_Kl_ayUA2D0Cw',
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
