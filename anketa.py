from telegram import ParseMode, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ConversationHandler
from utils import create_fox_keyboard


def anketa_start(update, context):
    update.message.reply_text(
        "Привет, пользователь! Представься пожалуйста, как тебя зовут?",
        reply_markup=ReplyKeyboardRemove()
    )

    # возвращаем имя первого ключа словаря states
    return "name"


def anketa_name(update, context):
    user_name = update.message.text
    if len(user_name.split()) < 2:
        update.message.reply_text("Пожалуйста введи имя и фамилию!")
        return "name"

    context.user_data["anketa"] = {"name": user_name}

    reply_keyboard = [["1", "2", "3", "4", "5"]]
    update.message.reply_text(
        "Пожалуйста, оцени мою работу по шкале от 1 до 5",
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, True, True)
    )

    return "rating"


def anketa_rating(update, context):
    context.user_data["anketa"]["raiting"] = int(update.message.text)
    update.message.reply_text("Напиши мне пожалуйста комментарий по своей оценке, если хочешь, или нажми /skip чтобы пропустить этот шаг")
    return "comment"


def anketa_comment(update, context):
    context.user_data["anketa"]["comment"] = update.message.text

    user_text = format_anketa(context.user_data["anketa"])
    update.message.reply_text(
        user_text,
        reply_markup=create_fox_keyboard(),
        parse_mode=ParseMode.HTML
    )

    return ConversationHandler.END


def anketa_skip(update, context):
    user_text = format_anketa(context.user_data["anketa"])
    update.message.reply_text(
        user_text,
        reply_markup=create_fox_keyboard(),
        parse_mode=ParseMode.HTML
    )

    return ConversationHandler.END


def format_anketa(anketa):
    user_text = f"""<b>Твои имя и фамилия</b>: {anketa['name']}
<b>Твоя оценка</b>: {anketa["raiting"]}"""

    if "comment" in anketa:
        user_text += f"\n<b>Твой комментарий</b>: {anketa['comment']}"

    return user_text


def anketa_dontknow(update, context):
    update.message.reply_text("Я вас не понимаю :(")
