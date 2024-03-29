import logging
import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from config import config, bot_token
from database import create_stories_table, limit_users, insert_data, check_user_in_db, get_last_session, update_data
from info import story, bot_messages
from GPT import create_user_prompt, create_prompt, create_messages, send_request
from datetime import datetime

bot = telebot.TeleBot(token=bot_token)

users = {}


def create_buttons(list_buttons: list):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    for button in list_buttons:
        keyboard.add(KeyboardButton(button))

    return keyboard


@bot.message_handler(commands=['start'])
def say_start(message):
    bot.send_message(message.chat.id, f'{bot_messages['start']}')

    create_stories_table()
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    limit = limit_users()
    checked_user = check_user_in_db(user_id)
    if limit and not checked_user:
        bot.send_message(message.chat.id, f'{bot_messages['user_limit']}')
    else:
        insert_data(user_id, user_name)


@bot.message_handler(commands=['help'])
def say_help(message):
    bot.send_message(message.chat.id, f'{bot_messages['help']}')


@bot.message_handler(commands=['begin_story'])
def begin_story(message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    keyboard = create_buttons([story['characters']['BOB']['name'],
                               story['characters']['SPIDER']['name'],
                               story['characters']['ROBO_BARBIE']['name'],
                               story['characters']['RED_HOOT']['name']])

    users[user_id] = {
        'name': user_name,
        'session': 0,
        'character': '',
        'world': '',
        'genre': '',
        'additional_task': '',
        'tokens': 0,
        'task': '',
        'answer': '',
        'full_story': ''
    }
    bot.send_message(message.chat.id, f"Выберете главного героя:\n", reply_markup=keyboard)


@bot.message_handler(func=lambda message: message.text in [story['characters']['BOB']['name'],
                                                           story['characters']['SPIDER']['name'],
                                                           story['characters']['ROBO_BARBIE']['name'],
                                                           story['characters']['RED_HOOT']['name']])
def choice_character(message):
    keyboard = create_buttons([story['worlds']['CYBERTRON']['name'],
                               story['worlds']['GOTHAM_CITY']['name'],
                               story['worlds']['BIKINI_BOTTOM']['name'],
                               story['worlds']['PINEAPPLE_FOREST']['name']])
    user_id = message.from_user.id
    users[user_id]['character'] = message.text
    update_data(user_id, 'character', message.text)

    if message.text == story['characters']['BOB']['name']:
        bot.send_photo(message.chat.id, story['characters']['BOB']['image'])
        bot.send_message(message.chat.id, story['characters']['BOB']['description'])

    elif message.text == story['characters']['SPIDER']['name']:
        bot.send_photo(message.chat.id, story['characters']['SPIDER']['image'])
        bot.send_message(message.chat.id, story['characters']['SPIDER']['description'])

    elif message.text == story['characters']['ROBO_BARBIE']['name']:
        bot.send_photo(message.chat.id, story['characters']['ROBO_BARBIE']['image'])
        bot.send_message(message.chat.id, story['characters']['ROBO_BARBIE']['description'])

    elif message.text == story['characters']['RED_HOOT']['name']:
        bot.send_photo(message.chat.id, story['characters']['RED_HOOT']['image'])
        bot.send_message(message.chat.id, story['characters']['RED_HOOT']['description'])

    bot.send_message(message.chat.id, f'Выберете вселенную:\n', reply_markup=keyboard)


@bot.message_handler(func=lambda message: message.text in [story['worlds']['CYBERTRON']['name'],
                                                           story['worlds']['GOTHAM_CITY']['name'],
                                                           story['worlds']['BIKINI_BOTTOM']['name'],
                                                           story['worlds']['PINEAPPLE_FOREST']['name']])
def choice_world(message):
    keyboard = create_buttons([story['genre']['HORROR'],
                               story['genre']['COMEDY'],
                               story['genre']['DRAMA'],
                               story['genre']['FANTASY']])
    user_id = message.from_user.id
    users[user_id]['world'] = message.text
    update_data(user_id, 'world', message.text)

    if message.text == story['worlds']['CYBERTRON']['name']:
        bot.send_photo(message.chat.id, story['worlds']['CYBERTRON']['image'])
        bot.send_message(message.chat.id, story['worlds']['CYBERTRON']['description'])

    elif message.text == story['worlds']['GOTHAM_CITY']['name']:
        bot.send_photo(message.chat.id, story['worlds']['GOTHAM_CITY']['image'])
        bot.send_message(message.chat.id, story['worlds']['GOTHAM_CITY']['description'])

    elif message.text == story['worlds']['BIKINI_BOTTOM']['name']:
        bot.send_photo(message.chat.id, story['worlds']['BIKINI_BOTTOM']['image'])
        bot.send_message(message.chat.id, story['worlds']['BIKINI_BOTTOM']['description'])

    elif message.text == story['worlds']['PINEAPPLE_FOREST']['name']:
        bot.send_photo(message.chat.id, story['worlds']['PINEAPPLE_FOREST']['image'])
        bot.send_message(message.chat.id, story['worlds']['PINEAPPLE_FOREST']['description'])

    bot.send_message(message.chat.id, f'Пора определиться с жанром!\n', reply_markup=keyboard)


@bot.message_handler(func=lambda message: message.text in [story['genre']['HORROR'],
                                                           story['genre']['COMEDY'],
                                                           story['genre']['DRAMA'],
                                                           story['genre']['FANTASY']])
def choice_genre(message):
    user_id = message.from_user.id
    users[user_id]['genre'] = message.text
    update_data(user_id, 'genre', message.text)
    bot.send_message(message.chat.id, f'Вы вбрали жанр: {message.text}.')

    keyboard = create_buttons(['Продолжить без дополнений'])
    bot.send_message(message.chat.id, 'Если хотите добавить пожелания, напишите их или нажмите кнопку: ',
                     reply_markup=keyboard)
    bot.register_next_step_handler(message, check_additional_task)


def check_additional_task(message):
    user_id = message.from_user.id
    last_session = get_last_session(user_id)
    users[user_id]['session'] = last_session + 1
    update_data(user_id, 'sessions', users[user_id]['session'])
    users[user_id]['tokens'] = int(config['LIMITS']['MAX_TOKEN_IN_SESSION'])
    if message.text == 'Продолжить без дополнений':
        users[user_id]['additional_task'] = ''
    else:
        users[user_id]['additional_task'] = message.text

    keyboard = create_buttons(['Генерировать историю!'])
    update_data(user_id, 'additional', message.text)

    bot.send_message(message.chat.id, 'Все ваши пожелания учтены! Если хотите перевыбрать главного персонажа, '
                                      'воспользуйтесь командой /begin_story', reply_markup=keyboard)


@bot.message_handler(
    func=lambda message: message.text in ['Генерировать историю!', 'Продолжить историю!', 'Конец истории!'])
def generate_story(message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    last_session = get_last_session(user_id)
    if last_session >= int(config['LIMITS']['MAX_SESSION']):
        bot.send_message(message.chat.id, f'Вы истратили свой лимит сессий! \n'
                                          f'Максимальное количство сессий: {config['LIMITS']['MAX_SESSION']}')
        return

    else:
        user_prompt = create_user_prompt(users[user_id]['character'], users[user_id]['world'], users[user_id]['genre'])
        prompt = create_prompt(user_id, users, user_prompt)
        messages = create_messages(message.text, prompt, users[user_id]['answer'])

        if message.text == 'Конец истории!':
            gpt_response = send_request(messages)
            current_tokens = users[user_id]['tokens'] - gpt_response['used_token']
            users[user_id]['tokens'] = current_tokens
            users[user_id]['full_story'] += " " + gpt_response['message']
            users[user_id]['answer'] = gpt_response['message']
            now_time = str(datetime.now())

            insert_data(user_id, user_name, users[user_id]['session'], current_tokens, users[user_id]['character'],
                        users[user_id]['world'], users[user_id]['genre'], users[user_id]['additional_task'], prompt,
                        users[user_id]['answer'], now_time)

            bot.send_message(message.chat.id, gpt_response['message'])
            bot.send_message(message.chat.id, 'Конец! Для получения полной истории, '
                                              'воспользуйтес командой /full_story', reply_markup=ReplyKeyboardRemove())
            return
        else:
            gpt_response = send_request(messages)
            current_tokens = users[user_id]['tokens'] - gpt_response['used_token']
            users[user_id]['tokens'] = current_tokens

            if current_tokens < 0:
                bot.send_message(message.chat.id, 'У вас закончились токены')
                bot.send_message(message.chat.id, 'Воспользуйтес командой /full_story')
                return

            users[user_id]['full_story'] += " " + gpt_response['message']
            users[user_id]['answer'] = gpt_response['message']
            now_time = str(datetime.now())

            insert_data(user_id, user_name, users[user_id]['session'], current_tokens, users[user_id]['character'],
                        users[user_id]['world'], users[user_id]['genre'], users[user_id]['additional_task'], prompt,
                        users[user_id]['answer'], now_time)

            keyboard = create_buttons(['Продолжить историю!',
                                       'Конец истории!'])

            bot.send_message(message.chat.id, 'Генерирую ...', reply_markup=keyboard)
            bot.send_message(message.chat.id, gpt_response['message'])
            bot.send_message(message.chat.id,
                             f'У вас осталось {current_tokens} токенов из {config['LIMITS']['MAX_TOKEN_IN_SESSION']} ')
            bot.register_next_step_handler(message, generate_story)


@bot.message_handler(commands=['full_story'])
def full_story(message):
    user_id = message.from_user.id
    if not users[user_id]['full_story']:
        bot.send_message(message.chat.id, 'Для начала нужно сгенерировать историю. Для начала воспользуйтесь '
                                          'командой /begin_story')
    else:
        bot.send_message(message.chat.id, users[user_id]['full_story'])


@bot.message_handler(commands=['debug'])
def send_logs(message):
    with open("log_file.txt", "rb") as f:
        bot.send_document(message.chat.id, f)
        logging.info("Use command DEBUG")


bot.polling()
