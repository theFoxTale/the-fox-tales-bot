from anketa import (
    anketa_comment,
    anketa_dontknow,
    anketa_name,
    anketa_rating,
    anketa_skip,
    anketa_start
)

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

from telegram.ext import (
    CommandHandler,
    ConversationHandler,
    Filters,
    MessageHandler,
    Updater
)

# Логи
logging.basicConfig(filename='theFoxTalesBot.log', level=logging.INFO)


def main():
    # Создаем бота и передаем ему ключ для авторизации на серверах Telegram
    mybot = Updater(settings.API_KEY, use_context=True)

    # Обработчики событий
    dp = mybot.dispatcher

    # обработчик диалогов с пользователем
    anketa = ConversationHandler(
        entry_points=[
            MessageHandler(Filters.regex('^(Заполнить анкету)$'), anketa_start)
        ],
        states={
            "name": [MessageHandler(Filters.text, anketa_name)],
            "rating": [MessageHandler(Filters.regex("^(1|2|3|4|5)$"), anketa_rating)],
            "comment": [
                CommandHandler("skip", anketa_skip),
                MessageHandler(Filters.text, anketa_comment)
            ]
        },
        fallbacks=[
            MessageHandler(Filters.text | Filters.photo | Filters.video | Filters.document | Filters.location, anketa_dontknow)
        ]
    )
    dp.add_handler(anketa)

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
    dp.add_handler(MessageHandler(
        Filters.regex('^(Картинка котика)$'),
        send_picture_with_cat
    ))
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
