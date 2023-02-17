import telebot

from config.config import BOT_API_TOKEN
from utils.jsonwork import get_json, take_info, student_json
from utils.keyboard import keyboard



global group_number

bot = telebot.TeleBot(BOT_API_TOKEN)


@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, 'Пожалуйста, введите номер учебной группы:')
    bot.register_next_step_handler(message, dates)




def dates(message):
    global group_number
    group_number = message.text
    message = bot.reply_to(message, "Выбирите неделю", reply_markup=keyboard)
    bot.register_next_step_handler(message,test)


def test(message):
    week = message.text
    student_json(group_number, week)
    get_json()
    msg = take_info()
    bot.send_message(message.chat.id, msg)


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