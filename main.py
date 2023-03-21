import telebot

from config.config import BOT_API_TOKEN
from utils.jsonwork import schedule
from utils.keyboard import keyboard



global group_number

bot = telebot.TeleBot(BOT_API_TOKEN)

MESS_MAX_LENGTH = 4096

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, 'Пожалуйста, введите номер учебной группы:')
    bot.register_next_step_handler(message, day)




def day(message):
    global group_number
    group_number = message.text
    message = bot.reply_to(message, "Выбирите день", reply_markup=keyboard)
    bot.register_next_step_handler(message,group_number_def)


def group_number_def(message):
    day = message.text
    raspisanie = schedule(group_number, day)
    for x in range(0, len(raspisanie), MESS_MAX_LENGTH):
        shraspis = raspisanie[x: x + MESS_MAX_LENGTH]
        bot.send_message(message.chat.id, shraspis)



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