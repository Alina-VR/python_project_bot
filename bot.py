import telebot
import config

bot = telebot.TeleBot(config.TOKEN)


@bot.message_handler(commands=['start'])
def welcome(message):
    sticker = open('sticker.tgs', 'rb')
    bot.send_sticker(message.chat.id, sticker)
    bot.send_message(message.chat.id, 'Добро пожаловать, {0.first_name}!\nЯ - {1.first_name}, '
                                      'помогу тебе распланировать время и не забыть ничего важного.'.
                     format(message.from_user, bot.get_me()))


@bot.message_handler(content_types=['text'])
def echo(message):
    bot.send_message(message.chat.id, 'Извините, пока не понимаю(')


bot.polling(none_stop=True)
