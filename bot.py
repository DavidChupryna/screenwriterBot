import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from config import token, config
from database import create_stories_table, limit_users, insert_data, check_user_in_db, get_last_session, update_data
from info import story

bot = telebot.TeleBot(token=token)

users = {}


def create_buttons(list_buttons: list):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    for button in list_buttons:
        keyboard.add(KeyboardButton(button))

    return keyboard


@bot.message_handler(commands=['start'])
def say_start(message):
    bot.send_message(message.chat.id, "Привет ..........................")

    create_stories_table()
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    limit = limit_users()
    checked_user = check_user_in_db(user_id)
    if limit and not checked_user:
        bot.send_message(message.chat.id, "Нет токенов")
    else:
        bot.send_message(message.chat.id, f"Добро пожаловать {user_name}, команда /begin_story")# добавить функцию help
        insert_data(user_id, user_name)


@bot.message_handler(commands=['help'])
def say_help(message):
    bot.send_message(message.chat.id,"/help ??????????????????????????????")


@bot.message_handler(commands=['begin_story'])
def begin_story(message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    last_session = get_last_session(user_id)
    if last_session >= int(config['LIMITS']['MAX_SESSION']):
        bot.send_message(message.chat.id, f'Вы истратили свой лимит сессий! \n'
                                          f'Максимальное количство сессий: {config['LIMITS']['MAX_SESSION']}')
        return
    else:
        update_data(user_id, 'sessions', last_session + 1)
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
        bot.send_message(message.chat.id,f"Выберете главного героя:\n"
                                        f"{story['characters']['BOB']['name']} - {story['characters']['BOB']['description']}. \n"
                                        f"{story['characters']['SPIDER']['name']} - {story['characters']['SPIDER']['description']}. \n"
                                        f"{story['characters']['ROBO_BARBIE']['name']} - {story['characters']['ROBO_BARBIE']['description']}. \n"
                                        f"{story['characters']['RED_HOOT']['name']} - {story['characters']['RED_HOOT']['description']}.", reply_markup=keyboard)


@bot.message_handler(func=lambda message: message.text in [story['characters']['BOB']['name'],
                               story['characters']['SPIDER']['name'],
                               story['characters']['ROBO_BARBIE']['name'],
                               story['characters']['RED_HOOT']['name']])
def choose_genre(message):
    keyboard = create_buttons([story['worlds']['CYBERTRON']['name'],
                               story['worlds']['GOTHAM_CITY']['name'],
                               story['worlds']['BIKINI_BOTTOM']['name'],
                               story['worlds']['PINEAPPLE_FOREST']['name']])
    user_id = message.from_user.id
    users[user_id]['character'] = message.text
    if message.text == story['characters']['BOB']['name']:
        bot.send_photo(message.chat.id, story['characters']['BOB']['image'])
        bot.send_message(message.chat.id, f'Вы выбрали {story['characters']['BOB']['name']} как главного героя!')
    elif message.text == story['characters']['SPIDER']['name']:
        bot.send_photo(message.chat.id, story['characters']['SPIDER']['image'])
        bot.send_message(message.chat.id, f'Вы выбрали {story['characters']['SPIDER']['name']} как главного героя!')
    elif message.text == story['characters']['ROBO_BARBIE']['name']:
        bot.send_photo(message.chat.id, story['characters']['ROBO_BARBIE']['image'])
        bot.send_message(message.chat.id, f'Вы выбрали {story['characters']['ROBO_BARBIE']['name']} как главного героя!')
    elif message.text == story['characters']['RED_HOOT']['name']:
        bot.send_photo(message.chat.id, story['characters']['RED_HOOT']['image'])
        bot.send_message(message.chat.id, f'Вы выбрали {story['characters']['RED_HOOT']['name']} как главного героя!')

    bot.send_message(message.chat.id, f'Выберете вселенную!\n'
                                      f'{story['worlds']['CYBERTRON']['name']} - {story['worlds']['CYBERTRON']['description']}\n'
                                      f'{story['worlds']['GOTHAM_CITY']['name']} - {story['worlds']['GOTHAM_CITY']['description']}\n'
                                      f'{story['worlds']['BIKINI_BOTTOM']['name']} - {story['worlds']['BIKINI_BOTTOM']['description']}\n'
                                      f'{story['worlds']['PINEAPPLE_FOREST']['name']} - {story['worlds']['PINEAPPLE_FOREST']['description']}', reply_markup=keyboard)


# @bot.message_handler(func=lambda message: message.text in [story['worlds']['CYBERTRON']['name'],
#                                                             story['worlds']['GOTHAM_CITY']['name'],
#                                                             story['worlds']['BIKINI_BOTTOM']['name'],
#                                                             story['worlds']['PINEAPPLE_FOREST']['name']])


bot.polling()