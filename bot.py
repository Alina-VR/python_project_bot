import datetime

import telebot
import config
from bot_db import BotDB, DELTA_UTC

bot_db = BotDB('database.db')
bot = telebot.TeleBot(config.TOKEN)


@bot.message_handler(commands=['start'])
def welcome(message):
    if not bot_db.is_user_in_db(message.from_user.id):
        bot_db.add_user(message.from_user.id)
    sticker = open('hello-sticker.tgs', 'rb')
    bot.send_sticker(message.chat.id, sticker)
    bot.send_message(message.chat.id, 'Добро пожаловать, {0.first_name}!\nЯ - {1.first_name}, '
                                      'помогу тебе распланировать время и не забыть ничего важного. Чтобы узнать, что '
                                      'я могу - пиши /help.'.
                     format(message.from_user, bot.get_me()))


@bot.message_handler(commands=['record_event'])
def record_event(message):
    hold_message = bot.send_message(message.chat.id, 'Напиши событие, которое хочешь записать, и его дату и время '
                                                     'в формате: yyyy mm dd hh mm')
    bot.register_next_step_handler(hold_message, add_event_with_feedback)


def add_event_with_feedback(message):
    bot_db.add_event(message)
    bot.send_message(message.chat.id, 'Отлично, событие записано!')


@bot.message_handler(commands=['today_events'])
def show_events(message):
    records = bot_db.get_events(message.from_user.id, 'day')
    if len(records):
        answer = 'Все события за день \n'
        for r in records:
            answer += 'Событие: ' + r[2] + ', '
            answer += 'Время: ' + str(datetime.datetime.fromisoformat(r[3]) + DELTA_UTC) + '\n'
        bot.send_message(message.chat.id, answer)
    else:
        bot.send_message(message.chat.id, 'Ещё нет событий. Давай что-нибудь запишем?')


@bot.message_handler(commands=['month_events'])
def show_events(message):
    records = bot_db.get_events(message.from_user.id, 'month')
    if len(records):
        answer = 'Все события за месяц \n'
        for r in records:
            answer += 'Событие: ' + r[2] + ', '
            answer += 'Время: ' + str(datetime.datetime.fromisoformat(r[3]) + DELTA_UTC) + '\n'
        bot.send_message(message.chat.id, answer)
    else:
        bot.send_message(message.chat.id, 'Ещё нет событий. Давай что-нибудь запишем?')


@bot.message_handler(commands=['all_events'])
def show_events(message):
    records = bot_db.get_events(message.from_user.id, 'all')
    if len(records):
        answer = 'Все события \n'
        for r in records:
            answer += 'Событие: ' + r[2] + ', '
            answer += 'Время: ' + str(datetime.datetime.fromisoformat(r[3]) + DELTA_UTC) + '\n'
        bot.send_message(message.chat.id, answer)
    else:
        bot.send_message(message.chat.id, 'Ещё нет событий. Давай что-нибудь запишем?')


@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, 'Давай я расскажу тебе, что я могу😊\nКак только ты напишешь мне /start - я '
                                      'запомню тебя, и смогу запоминать также твои события.\nПиши /record_event чтобы '
                                      'записать событие.\n Если хочешь вспомнить свои события за день - '
                                      'пиши /today_events, за месяц - /month_events, за всё время - /all_events.\n '
                                      'Если не помнишь, как мне написать - набери /help и увидишь все мои команды.')


@bot.message_handler(content_types=['text'])
def answer(message):
    bot.send_message(message.chat.id, 'Извини, пока не понимаю')
    sticker = open('sorry_sticker.tgs', 'rb')
    bot.send_sticker(message.chat.id, sticker)


bot.polling(none_stop=True)
