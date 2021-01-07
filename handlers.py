from clarifai.rest import ClarifaiApp
from glob import glob
import logging
import os
from random import choice
import settings

from utils import create_fox_keyboard, get_smile, play_game_random_numbers


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

    # ID чата с конкретным пользователем
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


def check_user_photo(update, context):
    update.message.reply_text("Лисичка получила твоё фото, обрабатываю фотографию... ")
    os.makedirs('downloads', exist_ok=True)

    # берём фото самого большого размера
    user_photo = context.bot.getFile(update.message.photo[-1].file_id)
    full_file_name = os.path.join("downloads", f"{user_photo.file_id}.jpg")
    user_photo.download(full_file_name)

    # проверяем, есть ли на фото котик
    if is_cat(full_file_name):
        update.message.reply_text("Лисичка нашла на фотографии котика, сейчас добавлю его в библиотеку!")
        new_file_name = os.path.join("images", f"cat_{user_photo.file_id}.jpg")
        os.rename(full_file_name, new_file_name)
    else:
        update.message.reply_text("Лисичка не увидела на фотографии котика :(")
        os.remove(full_file_name)


def is_cat(file_name):
    app = ClarifaiApp(api_key=settings.CLARIFAI_API_KEY)
    model = app.public_models.general_model
    response = model.predict_by_filename(file_name, max_concepts=5)

    # 10000 -код успешного ответа
    if response["status"]["code"] != 10000:
        return False

    for concept in response["outputs"][0]["data"]["concepts"]:
        if concept['name'] == 'cat':
            return True

    return False
