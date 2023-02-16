## generate keyboard here
import urllib.request

from telebot import types
from utils.jsonwork import get_dates
get_dates()




with open('utils/dateslist', 'r') as f:
    dates = [line.strip() for line in f]

keyboard = types.ReplyKeyboardMarkup(row_width=1)
for item in dates:
    keyboard.add(item)