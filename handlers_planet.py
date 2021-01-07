from datetime import date
import ephem

from utils import create_fox_keyboard


def print_planet_place(update, context):
    user_text = update.message.text
    text_data = user_text.split()
    if not len(text_data) > 1:
        return update.message.reply_text(
            "Эй, ты забыл дать мне название планеты, так я ничего не найду!")

    planet_name = text_data[1].strip()
    if not hasattr(ephem, planet_name):
        return update.message.reply_text(
            "К сожалению Лисичка не знает такую планету :(")

    # 'Mars', 'Earth', 'Mercury', 'Venus', 'Jupiter',
    # 'Neptune', 'Saturn', 'Uranus', 'Pluto'
    planet_data = getattr(ephem, planet_name)
    current_date = date.today()
    planet_data = planet_data(current_date)
    constellation = ephem.constellation(planet_data)
    update.message.reply_text(
        f'Планета *{planet_name}* сейчас в *{constellation}*.',
        parse_mode='MARKDOWN',
        reply_markup=create_fox_keyboard()
    )
