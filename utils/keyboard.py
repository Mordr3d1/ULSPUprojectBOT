## generate keyboard here
import urllib.request

from telebot import types




def date_day():
    with  open('dateslist.txt', 'w+') as file:
        file.write('Сегодня' + '\n')
        file.write('Завтра' + '\n')
        file.write('На неделю')

   # Выбор дня
date_day()



with open('dateslist.txt', 'r') as f:
    dates = [line.strip('') for line in f]



keyboard = types.ReplyKeyboardMarkup(row_width=1, one_time_keyboard=True)
for item in dates:
    keyboard.add(item)