import telebot
import config
from bot_db import BotDB

bot_db = BotDB('database.db')
bot = telebot.TeleBot(config.TOKEN)


@bot.message_handler(commands=['start'])
def welcome(message):
    if not bot_db.is_user_in_db(message.from_user.id):
        bot_db.add_user(message.from_user.id)
    sticker = open('sticker.tgs', 'rb')
    bot.send_sticker(message.chat.id, sticker)
    bot.send_message(message.chat.id, 'Добро пожаловать, {0.first_name}!\nЯ - {1.first_name}, '
                                      'помогу тебе распланировать время и не забыть ничего важного.'.
                     format(message.from_user, bot.get_me()))


@bot.message_handler(commands=['record_event'])
def record_event(message):
    hold_message = bot.send_message(message.chat.id, 'Напиши событие, которое хочешь записать, и его дату и время '
                                                     'в формате: yyyy mm dd hh mm')
    bot.register_next_step_handler(hold_message, add_event_with_feedback)


def add_event_with_feedback(message):
    bot_db.add_event(message)
    bot.send_message(message.chat.id, 'Отлично, событие записано!')


@bot.message_handler(content_types=['text'])
def answer(message):
    bot.send_message(message.chat.id, 'Извини, пока не понимаю(')


bot.polling(none_stop=True)
