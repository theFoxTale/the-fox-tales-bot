from emoji import emojize
from random import randint, choice
import settings
from telegram import ReplyKeyboardMarkup, KeyboardButton

def get_smile(user_data):
    if 'emoji' not in user_data:
        smile = choice(settings.USER_EMOJI)
        return emojize(smile, use_aliases=True)
    return user_data['emoji']

def play_game_random_numbers(user_number):
    bot_number = randint(user_number-10, user_number+10)
    if user_number > bot_number:
        message = f"Ты загадал {user_number}, Лисичка загадала {bot_number}. Ты выиграл!"
    elif user_number == bot_number:
        message = f"Ты загадал {user_number}, Лисичка загадала {bot_number}. У нас ничья!"
    else:
        message = f"Ты загадал {user_number}, Лисичка загадала {bot_number}. Я выиграла!"
    return message

def create_fox_keyboard():
    return ReplyKeyboardMarkup([
        ['Картинка котика', KeyboardButton('Мои координаты', request_location=True)]
    ])