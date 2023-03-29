import telebot

import datetime

from config.config import BOT_API_TOKEN
from utils.jsonwork import schedule
from utils.keyboard import keyboard

from datetime import date

from utils.Test import student_json,get_json,take_info

global group_number

global week

bot = telebot.TeleBot(BOT_API_TOKEN)

MESS_MAX_LENGTH = 4096

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, 'Пожалуйста, введите номер учебной группы:')
    bot.register_next_step_handler(message, day_of_week)




def day_of_week(message):
    global group_number
    group_number = message.text
    message = bot.reply_to(message, "Выбирите день", reply_markup=keyboard)
    bot.register_next_step_handler(message,group_number_def)


def group_number_def(message):
    day = message.text
    if day == 'На неделю':
        d1 = date(2022, 8, 26)
        d2 = datetime.date.today()
        day = (d1 - d2).days // 7
        day = day *(-1)
        student_json(group_number,day)
        get_json()
        msg = take_info()
        bot.send_message(message.chat.id,msg)

    elif  day == 'На две недели':
        d1 = date(2022, 8, 26)
        d2 = datetime.date.today()
        day = (d1 - d2).days // 7
        day = day *(-1)
        student_json(group_number,day)
        get_json()
        msg = take_info()
        bot.send_message(message.chat.id,msg)

        d1 = date(2022, 8, 26)
        d2 = datetime.date.today()
        day = (d1 - d2).days // 7
        day = day *(-1)
        day = day + 1
        student_json(group_number,day)
        get_json()
        msg = take_info()
        bot.send_message(message.chat.id,msg)

    else:
        raspisanie = schedule(group_number, day)
        for x in range(0, len(raspisanie), MESS_MAX_LENGTH):
            shraspis = raspisanie[x: x + MESS_MAX_LENGTH]
            bot.send_message(message.chat.id, shraspis, parse_mode ='Markdown')



@bot.message_handler(commands=['help'])
def start(message):
    bot.send_message(message.chat.id, 'Help command')




## should be at the bottom, after all other function
@bot.message_handler(func=lambda messages: True)
def any_message(message):
    msg = "Cannot understand you. Please, enter '/help' or '/start' "
    bot.reply_to(message, msg)



## load next step handlers if needed here
if __name__ == "__main__":
    bot.enable_save_next_step_handlers(delay=2)
    bot.load_next_step_handlers()
    bot.infinity_polling()