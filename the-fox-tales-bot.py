import logging
import ephem
import settings

from datetime import date
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Логи
logging.basicConfig(filename='theFoxTalesBot.log', level=logging.INFO)

def greet_user(update, context):
    print('Вызван /start')
    update.message.reply_text('Здравствуй, пользователь! Ты вызвал команду /start')

def talk_to_me(update, context):
    user_text = update.message.text 
    update.message.reply_text(f"Ты говоришь Лисичке *{user_text}*.\nИ Лисичка отвечает тебе _{user_text}_!", parse_mode='MARKDOWN')

def print_planet_place(update, context):
    user_text = update.message.text
    text_data = user_text.split()
    if not len(text_data) > 1:
        return update.message.reply_text("Эй, ты забыл дать мне название планеты, так я ничего не найду!")
        
    planet_name = text_data[1].strip()
    if not hasattr(ephem, planet_name):   
        return update.message.reply_text("К сожалению Лисичка не знает такую планету :(")

    #'Mars', 'Earth', 'Mercury', 'Venus', 'Jupiter', 'Neptune', 'Saturn', 'Uranus', 'Pluto'
    planet_data = getattr(ephem, planet_name)
    current_date = date.today()
    planet_data = planet_data(current_date)
    constellation = ephem.constellation( planet_data )
    update.message.reply_text(f'Планета *{planet_name}* сейчас в *{constellation}*.', parse_mode='MARKDOWN')

def get_wordcount(update, context):
    user_text = update.message.text
    user_text = user_text.replace("/wordcount", '')
    print(user_text)
    if not isinstance(user_text, str):
        return update.message.reply_text('Ой, кажется ты ввёл не строку')
    
    stripped_text = user_text.strip()
    if len(stripped_text) == 0:
        return update.message.reply_text('Похоже ты ввёл пустую строку!')

    res_text = stripped_text.split()
    update.message.reply_text(f'Лисичка посчитала, в твоей строке {len(res_text)} слов!')

def main():
    # Создаем бота и передаем ему ключ для авторизации на серверах Telegram
    mybot = Updater(settings.API_KEY, use_context=True)

    # Обработчики событий
    dp = mybot.dispatcher
    dp.add_handler(CommandHandler("start", greet_user))
    dp.add_handler(CommandHandler("planet", print_planet_place))
    dp.add_handler(CommandHandler("wordcount", get_wordcount))
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