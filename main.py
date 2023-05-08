import telebot

from config.config import BOT_API_TOKEN
from utils.jsonwork import *

from utils.keyboard import *


bot = telebot.TeleBot(BOT_API_TOKEN)

MESS_MAX_LENGTH = 3000

group_number = ''

def send_schedule(listRaspis, message):
    raspis = listRaspis[0]
    for x in range(1, len(listRaspis)):
        if len(raspis + listRaspis[x]) < MESS_MAX_LENGTH:
            raspis += listRaspis[x]
        else:
            bot.send_message(message.chat.id, raspis, parse_mode='Markdown', reply_markup=telebot.types.ReplyKeyboardRemove())
            raspis = listRaspis[x]
    if raspis:
        bot.send_message(message.chat.id, raspis, parse_mode='Markdown', reply_markup=telebot.types.ReplyKeyboardRemove())


@bot.message_handler(commands=['start'])
def gr_start(message):
    bot.reply_to(message, 'Пожалуйста, введите номер учебной группы:')
    bot.register_next_step_handler(message, gr_day_of_week)


def gr_day_of_week(message):
    global group_number
    group_number = group(message.text)
    if group_number:
        message = bot.reply_to(message, "Выбирите временной промежуток", reply_markup=chois_buttons())
        bot.register_next_step_handler(message,group_schedule)
    else:
        bot.send_message(message.chat.id, 'Данной учебной группы не существует')


def group_schedule(message):
    global group_number
    msg = message.text
    if msg == 'на сегодня':
        listRaspis = gr_today_raspis(group_number)
        send_schedule(listRaspis, message)
    elif msg == 'на завтра':
        listRaspis = gr_tomorrow_raspis(group_number)
        send_schedule(listRaspis, message)
    elif msg == 'на эту неделю':
        listRaspis = gr_this_week_schedule(group_number)
        send_schedule(listRaspis, message)
    elif msg == 'на следующую неделю':
        listRaspis = gr_next_week_schedule(group_number)
        send_schedule(listRaspis, message)


@bot.message_handler(commands=['help'])
def start(message):
    bot.send_message(message.chat.id, 'Help command')


## should be at the bottom, after all other function
@bot.message_handler(func=lambda messages: True)
def any_message(message):
    msg = "Не корректно введено сообщение, введите '/help' or '/start' "
    bot.reply_to(message, msg)

    

## load next step handlers if needed here
if __name__ == "__main__":
    bot.infinity_polling()
