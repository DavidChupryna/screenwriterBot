import configparser

config = configparser.ConfigParser()
config['LOGGING'] = {
    'level': 'INFO',
    'format': '%%(asctime)s - %%(name)s - %%(levelname)s - %%(message)s',
    'filename': 'log_file.txt',
    'filemod': 'w'
    }

config['GPT'] = {
    'URL': 'http://localhost:1234/v1/chat/completions',
    'TEMPERATURE': '0.6',
    'MAX_TOKENS': '64',
    }

config['LIMITS'] = {
    'MAX_MESSAGE_TOKENS': '50',
    'MAX_USERS': '2',
    'MAX_SESSION': '3',
    'MAX_TOKEN_IN_SESSION': '1000'
    }

config['PROMPTS'] = {
    'SYSTEM': 'Ты пишешь историю по заданым пользователем параметрам. Начинает пользовватель, а ты продолжаешь.'
                    ' В историю можешь добавлять диалоги между пресонажами. Диалоги пиши с новой строки и отделяй тире.'
                    'В истории не приветствуется пояснительный текст.',
    'END': 'Напиши логическое завершение истории c неожиданной развязкой. Не добавляй пояснительный текст',
    'CONTINUE': 'Логически продолжи сюжет в 1-3 предложения, держи интригу. Не добавляй пояснительный текст'
}
token = '7184586489:AAHavezhvXtnqkWqTXCzEGLN3efnL-y0BI4'
