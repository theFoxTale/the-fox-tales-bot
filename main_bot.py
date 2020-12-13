from handlers import (
    greet_user, 
    talk_to_me, 
    get_wordcount, 
    guess_number, 
    send_picture_with_cat,
    get_user_coordinates,
    check_user_photo
)
from handlers_planet import print_planet_place

import logging
import settings
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Логи
logging.basicConfig(filename='theFoxTalesBot.log', level=logging.INFO)

def main():
    # Создаем бота и передаем ему ключ для авторизации на серверах Telegram
    mybot = Updater(settings.API_KEY, use_context=True)

    # Обработчики событий
    dp = mybot.dispatcher
    # обработчики команд
    dp.add_handler(CommandHandler("start", greet_user))
    dp.add_handler(CommandHandler("planet", print_planet_place))
    dp.add_handler(CommandHandler("wordcount", get_wordcount))
    dp.add_handler(CommandHandler("guess", guess_number))
    dp.add_handler(CommandHandler("cat", send_picture_with_cat))

    # обработчик фото
    dp.add_handler(MessageHandler(Filters.photo, check_user_photo))

    # обработчики текста
    # более частные всегда ставим выше, более общие - внизу
    dp.add_handler(MessageHandler(Filters.regex('^(Картинка котика)$'), send_picture_with_cat))
    dp.add_handler(MessageHandler(Filters.location, get_user_coordinates))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))

    # Командуем боту начать ходить в Telegram за сообщениями
    logging.info("Бот стартовал!")
    mybot.start_polling()
    # Запускаем бота, он будет работать, пока мы его не остановим принудительно
    mybot.idle()


# Исполняется только при прямом вызове файла python bot.py 
# и не вызывается при импорте, например from bot import PROXY
if __name__ == "__main__":
    main()