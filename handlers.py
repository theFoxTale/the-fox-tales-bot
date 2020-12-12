from glob import glob
import logging
from random import choice

from utils import get_smile, play_game_random_numbers, create_fox_keyboard

def greet_user(update, context):
    logging.info('Вызван /start')
    context.user_data['emoji'] = get_smile(context.user_data)
    update.message.reply_text(
        f"Здравствуй, пользователь {context.user_data['emoji']}! Ты вызвал команду /start",
        reply_markup=create_fox_keyboard()
    )

def talk_to_me(update, context):
    context.user_data['emoji'] = get_smile(context.user_data)
    user_text = update.message.text
    update.message.reply_text(
        f"Ты говоришь Лисичке *{user_text}*.\nИ Лисичка отвечает тебе _{user_text}_! {context.user_data['emoji']}", parse_mode='MARKDOWN',
        reply_markup=create_fox_keyboard()
    )

def get_wordcount(update, context):
    user_text = update.message.text
    user_text = user_text.replace("/wordcount", '')
    logging.info(user_text)
    if not isinstance(user_text, str):
        return update.message.reply_text('Ой, кажется ты ввёл не строку')
    
    stripped_text = user_text.strip()
    if len(stripped_text) == 0:
        return update.message.reply_text('Похоже ты ввёл пустую строку!')

    res_text = stripped_text.split()
    update.message.reply_text(
        f'Лисичка посчитала, в твоей строке {len(res_text)} слов!',
        reply_markup=create_fox_keyboard()
    )

def guess_number(update, context):
    logging.info(context.args)
    if not context.args:
        update.message.reply_text('Лисичка расстроена, ты не ввёл никакого числа!')

    try:
        user_number = int(float(context.args[0]))
        update.message.reply_text(play_game_random_numbers(user_number))
    except (ValueError, TypeError):
        update.message.reply_text(f'Эй, ты ввёл текст {context.args[0]}, а не число!')

def send_picture_with_cat(update, context):
    cat_images_list = glob('images/cat-*.jp*g')
    cat_filename = choice(cat_images_list)

    #ID чата с конкретным пользователем
    chat_id = update.effective_chat.id
    context.bot.send_photo(
        chat_id=chat_id, 
        photo=open(cat_filename, 'rb'),
        reply_markup=create_fox_keyboard()
    )

def get_user_coordinates(update, context):
    context.user_data['emoji'] = get_smile(context.user_data)
    coords = update.message.location
    update.message.reply_text(
        f"Лисичка нашла твои координаты {context.user_data['emoji']}: долгота {coords['longitude']}, широта {coords['latitude']}!",
        reply_markup=create_fox_keyboard()
    )
